from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
import time
import datetime

import apps.notifier.keyboards as keyboards
from apps.notifier.state import MakeMessage, Notifier
from apps.notifier.models import save_message


async def make_messages(message: types.Message):
    await message.answer('Введи текст сообщения')
    await MakeMessage.waiting_for_text.set()


async def add_text(message: types.Message, state: FSMContext):
    await state.update_data(text=message.text)
    keyboard = keyboards.yes_no_keyboard()
    await MakeMessage.next()
    await message.answer('Все верно написано?', reply_markup=keyboard)


async def check_text(message: types.Message):
    if message.text.lower() == 'нет':
        await message.answer('Ну тогда напиши текст еще раз, но уже правильно!')
        await MakeMessage.waiting_for_text.set()
    elif message.text.lower() == 'да':
        await MakeMessage.next()
        keyboard = keyboards.how_often_keyboard()
        await message.answer('Как часто повторять?', reply_markup=keyboard)
    else:
        keyboard = keyboards.yes_no_keyboard()
        await message.answer('Тебя по русски спрашивают. Да или Нет...\n'
                             'Для таких людей как ты есть даже кнопки внизу для ответа', reply_markup=keyboard)
        return


async def add_time_repeat(message: types.Message, state: FSMContext):
    variants = ['ежедневно',
                'еженедельно',
                'ежемесячно',
                ]
    if message.text.lower() not in variants:
        await message.answer('Просто..нажми..на кнопку...')
        return
    await state.update_data(periodicity=message.text.lower())
    await MakeMessage.next()
    keyboard = keyboards.week_keyboard()
    await message.answer('С какого дня недели начнем?', reply_markup=keyboard)


async def add_day_of_the_week(message: types.Message, state: FSMContext):
    variants = ['понедельник',
                'вторник',
                'среда',
                'четверг',
                'пятница',
                'суббота',
                'воскресенье']
    if message.text.lower() not in variants:
        await message.answer('День недели!!! Еще раз пожалуйста')
    day_index = variants.index(message.text.lower())
    found_date = datetime.date.today()
    for i in range(7):
        if found_date.weekday() == day_index:
            break
        found_date += datetime.timedelta(days=1)
    await state.update_data(near_date=found_date)
    await MakeMessage.next()
    await message.answer('В какое время будем это делать? (формат: 15:45)')


async def add_time(message: types.Message, state: FSMContext):
    try:
        time.strptime(message.text, '%H:%M')
    except ValueError:
        await message.answer('формат времени чч:мм, попробуй еще раз')
        return
    need_time = message.text
    await state.update_data(time_publ=need_time)
    await MakeMessage.next()
    keyboard = keyboards.type_chat_keyboard()
    await message.answer('И последнее, в какой чат мы все это отправим', reply_markup=keyboard)


async def add_type_chat(message: types.Message, state: FSMContext):
    variants = ['преподавательский', 'ученический']
    if message.text.lower() not in variants:
        keyboard = keyboards.type_chat_keyboard()
        await message.answer('Пока только есть два чата, выберите из них (кнопки)', reply_markup=keyboard)
        return
    data = await state.get_data()
    date_now = datetime.datetime.now()
    if data['near_date'] == datetime.date.today():
        if data['time_publ'] < date_now.time().strftime('%H:%M'):
            data['near_date'] += datetime.timedelta(weeks=1)
    save_message(data['text'],
                 data['periodicity'],
                 data['near_date'].strftime('%d.%m.%y'),
                 data['time_publ'],
                 type_chat=message.text.lower()
                 )
    await state.finish()
    await Notifier.waiting_work_with_notifier.set()
    keyboard = keyboards.start_keyboard()
    await message.answer('Все супер, жди моих сообщений\n Возврат на начальную страницу', reply_markup=keyboard)


def register_make_messages(dp: Dispatcher):
    dp.register_message_handler(make_messages,
                                Text(equals='добавить', ignore_case=True),
                                state=Notifier.waiting_work_with_notifier)
    dp.register_message_handler(add_text, state=MakeMessage.waiting_for_text)
    dp.register_message_handler(check_text, state=MakeMessage.waiting_for_check_text)
    dp.register_message_handler(add_time_repeat, state=MakeMessage.waiting_how_often_repeat_text)
    dp.register_message_handler(add_day_of_the_week, state=MakeMessage.waiting_day_of_the_week)
    dp.register_message_handler(add_time, state=MakeMessage.waiting_time)
    dp.register_message_handler(add_type_chat, state=MakeMessage.waiting_type_chat)
