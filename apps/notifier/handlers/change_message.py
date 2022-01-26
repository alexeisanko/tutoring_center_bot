from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
import datetime
import time

import apps.notifier.keyboards as keyboards
from apps.notifier.state import ChangeMessage, Notifier
from apps.notifier.models import get_text_all_messages, get_message_by_text, change_message


async def show_messages(message: types.Message):
    await ChangeMessage.waiting_choice_message.set()
    text_messages = get_text_all_messages()
    keyboard = keyboards.messages_keyboard(text_messages)
    await message.answer('Какое сообщение хотите поменять?', reply_markup=keyboard)


async def come_back_menu(message: types.Message):
    await Notifier.waiting_work_with_notifier.set()
    keyboard = keyboards.start_keyboard()
    await message.answer('Изменеие завершено', reply_markup=keyboard)


async def uncover_message(message: types.Message, state: FSMContext):
    my_message = get_message_by_text(message.text)[0]
    if not my_message:
        await message.answer('Такого сообщения нету. Выберите сообщение из списка')
        return
    await ChangeMessage.next()
    await state.update_data(id_message=my_message[0])
    keyboard = keyboards.change_keyboard(my_message)
    await message.answer('Что будем менять?', reply_markup=keyboard)


async def come_back_to_change(message: types.Message):
    await ChangeMessage.waiting_choice_message.set()
    text_messages = get_text_all_messages()
    keyboard = keyboards.messages_keyboard(text_messages)
    await message.answer('Какое сообщение хотите поменять', reply_markup=keyboard)


async def add_change(message: types.Message, state: FSMContext):
    decode_commands = {'текст': ('text', None),
                       'периодичность': ('periodicity', keyboards.how_often_keyboard),
                       'ближайшая дата': ('near_data_publ', None),
                       'время': ('time_publ', None),
                       'тип чата': ('type_chat', keyboards.type_chat_keyboard),
                       }
    await ChangeMessage.next()
    command_user = message.text.lower().split(':')[0]
    column = decode_commands[command_user]
    await state.update_data(column=column)
    await message.answer('Введите новое значение', reply_markup=column[1]() if column[1] else None)


async def save_change(message: types.Message, state: FSMContext):
    data = await state.get_data()
    command = data['column'][0]
    if command == 'periodicity':
        variants = ['ежедневно',
                    'еженедельно',
                    'ежемесячно',
                    ]
        if message.text.lower() not in variants:
            await message.answer('Просто..нажми..на кнопку...',
                                 reply_markup=data['column'][1]() if data['column'][1] else None)
            return
    elif command == 'near_data_publ':
        try:
            datetime.datetime.strptime(message.text, '%d.%m.%y')
        except ValueError:
            await message.answer('формат даты 15.01.22, попробуй еще раз')
            return
    elif command == 'time_publ':
        try:
            time.strptime(message.text, '%H:%M')
        except ValueError:
            await message.answer('формат времени чч:мм, попробуй еще раз')
            return
    elif command == 'type_chat':
        variants = ['преподовательский', 'ученический']
        if message.text.lower() not in variants:
            await message.answer('Не верный тип чата, выбери из существующих',
                                 reply_markup=data['column'][1]() if data['column'][1] else None)
            return
    if command == 'text':
        change_message(command, message.text, data['id_message'])
    else:
        change_message(command, message.text.lower(), data['id_message'])
    await state.finish()
    await Notifier.waiting_work_with_notifier.set()
    keyboard = keyboards.start_keyboard()
    await message.answer('Изменение сохранено', reply_markup=keyboard)


def register_change_messages(dp: Dispatcher):
    dp.register_message_handler(show_messages,
                                Text(equals='изменить', ignore_case=True),
                                state=Notifier.waiting_work_with_notifier)
    dp.register_message_handler(come_back_menu,
                                Text(equals='назад', ignore_case=True),
                                state=ChangeMessage.waiting_choice_message)
    dp.register_message_handler(uncover_message, state=ChangeMessage.waiting_choice_message)
    dp.register_message_handler(come_back_to_change,
                                Text(equals='назад', ignore_case=True),
                                state=ChangeMessage.waiting_choice_change)
    dp.register_message_handler(add_change, state=ChangeMessage.waiting_choice_change)
    dp.register_message_handler(save_change, state=ChangeMessage.waiting_add_change)
