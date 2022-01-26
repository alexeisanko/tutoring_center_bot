from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

import apps.notifier.keyboards as keyboards
from apps.notifier.state import DeleteMessage, Notifier
from apps.notifier.models import get_text_all_messages, delete_message, get_message_by_text


async def show_messages(message: types.Message):
    await DeleteMessage.waiting_choice_message.set()
    text_messages = get_text_all_messages()
    keyboard = keyboards.messages_keyboard(text_messages)
    await message.answer('Какое сообщение хотите удалить?', reply_markup=keyboard)


async def come_back_menu(message: types.Message):
    await Notifier.waiting_work_with_notifier.set()
    keyboard = keyboards.start_keyboard()
    await message.answer('Работа с удалением завершена', reply_markup=keyboard)


async def aсcept_delete(message: types.Message, state: FSMContext):
    id_message = get_message_by_text(message.text)[0][0]
    await state.update_data(id_message=id_message)
    keyboard = keyboards.yes_no_keyboard()
    await DeleteMessage.next()
    await message.answer('Уверены?', reply_markup=keyboard)


async def delete_mes(message: types.Message, state: FSMContext):
    if message.text.lower() == 'нет':
        await DeleteMessage.waiting_choice_message.set()
        text_messages = get_text_all_messages()
        keyboard = keyboards.messages_keyboard(text_messages)
        await message.answer('Хорошо. Вернулись  назад. Какое сообщение хотите удалить?', reply_markup=keyboard)
    elif message.text.lower() == 'да':
        await DeleteMessage.waiting_choice_message.set()
        id_message = await state.get_data()
        delete_message(id_message['id_message'])
        text_messages = get_text_all_messages()
        keyboard = keyboards.messages_keyboard(text_messages)
        await message.answer('Сообщение удалено. Хотите еще что-то удалить?', reply_markup=keyboard)
    else:
        keyboard = keyboards.yes_no_keyboard()
        await message.answer('Тебя по русски спрашивают. Да или Нет...\n'
                             'Для таких людей как ты есть даже кнопки внизу для ответа', reply_markup=keyboard)
        return


def register_delete_messages(dp: Dispatcher):
    dp.register_message_handler(show_messages, Text(equals='удалить', ignore_case=True),
                                state=Notifier.waiting_work_with_notifier)
    dp.register_message_handler(come_back_menu,
                                Text(equals='назад', ignore_case=True),
                                state=DeleteMessage.waiting_choice_message)
    dp.register_message_handler(aсcept_delete, state=DeleteMessage.waiting_choice_message)
    dp.register_message_handler(delete_mes, state=DeleteMessage.waiting_accept_delete)

