from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


def start_keyboard() -> types.ReplyKeyboardMarkup:
    button_notifier = 'Рассылка сообщений'
    button_new = 'Экзамены (Разработка)'

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(button_notifier).add(button_new)
    return keyboard


async def cmd_start(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = start_keyboard()
    await message.answer('Вас приветствует личный бот репетиторского центра New School?\n'
                         'Что хотите сделать?', reply_markup=keyboard)


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    keyboard = start_keyboard()
    await message.answer('Отмена операции.\nВозврат в главное меню', reply_markup=keyboard)


def register_common(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands=['start'], state=['*'])
    dp.register_message_handler(cmd_cancel, commands=['cancel'], state=['*'])
    dp.register_message_handler(cmd_cancel, Text(equals='вернуться в главное меню', ignore_case=True), state=['*'])
