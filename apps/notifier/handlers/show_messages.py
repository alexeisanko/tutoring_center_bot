from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


import apps.notifier.keyboards as keyboards
from apps.notifier.state import ShowMessage, Notifier
from apps.notifier.models import get_text_all_messages, get_message_by_text


async def show_messages(message: types.Message):
    await ShowMessage.waiting_choice_message.set()
    text_messages = get_text_all_messages()

    keyboard = keyboards.messages_keyboard(text_messages)
    await message.answer('Что бы посмотреть подробности выберите любое сообщение', reply_markup=keyboard)


async def uncover_message(message: types.Message):
    my_message = get_message_by_text(message.text)
    if not my_message:
        await message.answer('Такого сообщения нету. Выберите сообщение из списка')
        return
    await message.answer(f'Текст:\n{my_message[0][1]}\n\n'
                         f'Периодичность: {my_message[0][2]}\n\n'
                         f'Ближайшая дата отправки\n{my_message[0][3]} {my_message[0][4]}\n\n'
                         f'Вид чата: {my_message[0][5]}')


async def come_back(message: types.Message):
    await Notifier.waiting_work_with_notifier.set()
    keyboard = keyboards.start_keyboard()
    await message.answer('Просмотр закрыт', reply_markup=keyboard)


def register_show_messages(dp: Dispatcher):
    dp.register_message_handler(show_messages,
                                Text(equals='посмотреть все', ignore_case=True),
                                state=Notifier.waiting_work_with_notifier)
    dp.register_message_handler(come_back,
                                Text(equals='назад', ignore_case=True),
                                state=ShowMessage.waiting_choice_message)
    dp.register_message_handler(uncover_message, state=ShowMessage.waiting_choice_message)

