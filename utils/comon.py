from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


def start_keyboard() -> types.ReplyKeyboardMarkup:
    button_add = 'Добавить сообщение'
    button_list = 'Посмотреть созданные сообщения'
    button_change = 'Изменить сообщение'
    button_remove = 'Удалить сообщения'
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(button_add).add(button_list).add(button_change).add(button_remove)
    return keyboard


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = start_keyboard()
    await message.answer('Вас приветствует личный бот репетиторского центра?\n'
                         'Что хотите сделать?', reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = start_keyboard()
    await message.answer('Операция отменена', reply_markup=keyboard)


def register_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state=['*'])
    dp.register_message_handler(cmd_cancel, commands=['cancel'], state=['*'])
    dp.register_message_handler(cmd_cancel, Text(equals='отмена', ignore_case=True), state=['*'])
