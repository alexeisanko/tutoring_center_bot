import datetime
import time

from aiogram import types, Dispatcher
from apps.notifier.models import get_sent_message
from config import CHAT_ID_TG

FLAG = False


async def begin_send_messages(message: types.Message):
    global FLAG
    FLAG = True
    await message.answer('Режим оповещения включен')
    while True:
        if not FLAG:
            return
        day_now = datetime.date.today().strftime('%d.%m.%y')
        time_now = datetime.datetime.now().strftime('%H:%M')
        messages = get_sent_message(day_now, time_now)
        if messages:
            for text in messages:
                await message.bot.send_message(CHAT_ID_TG, text[1])
                # TODO добавить изменения в БД (ближайщую дату)
        time.sleep(60)


async def stop_send_messages(message: types.Message):
    global FLAG
    FLAG = False
    await message.answer('Режим оповещения включен')
    return


def register_send_messages(dp: Dispatcher):
    dp.register_message_handler(begin_send_messages, commands=['start_notifier'], state=['*'])
    dp.register_message_handler(stop_send_messages, commands=['stop_notifier'], state=['*'])




