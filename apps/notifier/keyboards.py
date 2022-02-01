from aiogram import types


def start_keyboard(one_time=True) -> types.ReplyKeyboardMarkup:
    button_add = 'Добавить'
    button_list = 'Посмотреть все'
    button_change = 'Изменить'
    button_remove = 'Удалить'
    button_start = 'Включить рассылку'
    button_end = 'Остановить рассылку'
    button_main_menu = 'Вернуться в главное меню'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=one_time)
    keyboard.\
        add(button_add, button_list).\
        add(button_change, button_remove).\
        add(button_start).\
        add(button_end).\
        add(button_main_menu)
    return keyboard


def yes_no_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ['Да', 'Нет']
    keyboard.add(*buttons)
    return keyboard


def how_often_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ['Ежедневно',
               'Еженедельно',
               'Ежемесячно',
               ]
    for button in buttons:
        keyboard.add(button)
    return keyboard


def week_keyboard() -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    buttons = ['Понедельник',
               'Вторник',
               'Среда',
               'Четверг',
               'Пятница',
               'Суббота',
               'Воскресенье']
    for button in buttons:
        keyboard.add(button)
    return keyboard


def messages_keyboard(messages) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for message in messages:
        keyboard.add(message[0])
    keyboard.add('Назад')
    return keyboard


def change_keyboard(message) -> types.ReplyKeyboardMarkup:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    button_text = message[1]
    button_periodicity = message[2]
    button_near_data_publ = message[3]
    button_time_publ = message[4]
    button_type_chat = message[5]
    button_come_back = 'Назад'
    keyboard.add(f'Текст: {button_text}')
    keyboard.add(f'Периодичность: {button_periodicity}')
    keyboard.add(f'Ближайшая дата: {button_near_data_publ}')
    keyboard.add(f'Время: {button_time_publ}')
    keyboard.add(f'Тип чата: {button_type_chat}')
    keyboard.add(button_come_back)
    return keyboard


def type_chat_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add('Преподавательский').add('Ученический')
    return keyboard
