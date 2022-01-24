from aiogram import types


def start_keyboard() -> types.ReplyKeyboardMarkup:
    button_add = 'Добавить сообщение'
    button_list = 'Посмотреть созданные сообщения'
    button_change = 'Изменить сообщение'
    button_remove = 'Удалить сообщения'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(button_add).add(button_list).add(button_change).add(button_remove)
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
