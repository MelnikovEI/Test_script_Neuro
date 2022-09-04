nlu_call  # Полагаю, что это идентификатор конкретного диалога

nn = NeuroNetLibrary(nlu_call, event_loop)  # Создать объект диалога
nlu = NeuroNluLibrary(nlu_call, event_loop)  # Создать объект для обработки текста
nv = NeuroVoiceLibrary(nlu_call, loop)  # Создать объект для написания логики во время звонка

phrase_action = [  # Список словарей "phrase-action" для выбора следуюющего шага
    {  # Словарь для переходов при первом сообщении
    'NULL': 'hello_null',
    'DEFAULT': 'recommend_main',
    'Да': 'recommend_main',
    ...
    },
    {  # Словарь для переходов при повторе
    'NULL': 'hangup_null',
    ...
    }
]
# Список promt_name для выхода из диалога
hangup_logic_list = ['hangup_positive', 'hangup_negative', 'hangup_wrong_time', 'hangup_null', 'forward']
counter = 0  # Счетчик применений prompt_name
nn.call('номер абонента')  # Позвонить
prompt_name = 'hello'  # Первая фраза
while prompt_name not in hangup_logic_list:  # Пока не дошли до завершения диалога
    nv.say(prompt_name)  # Сказать текущую фразу, нужна проверка существования соответствующего аудио
    with nv.listen() as r:  """ Слушать ответ. Настроить параметры остановки текущего аудио (как я понимаю, если клиент
                                сказал что-то определенное. Здесь не понятна спецификация функции...
                                Требуется асинхронное поведение: пока гворим фразу - слушаем клиента
                            """
    r = nlu.extract(...)  # Получить ответ, сопоставить ему prompt_name
    nn.counter(prompt_name, '+')  # Увеличить счётчик применения prompt_name
    counter = nn.counter(prompt_name)
    prompt_name = phrase_action[counter - 1][r]  # result - результат разбора ответа, по нему выбираем следующий шаг
                                        # надо учесть в каком разделе "logic_unit" находимся в текущий момент

nv.say(prompt_name)  # Сказать завершающую фразу
if prompt_name == 'forward':  # Переключить на оператора
    bridge_action
else:
    hangup_action  # Завершить диалог

# Записать результаты
