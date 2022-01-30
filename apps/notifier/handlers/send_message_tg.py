import datetime
import asyncio
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text

from apps.notifier.models import get_sent_message, change_near_date
from apps.notifier.state import Notifier
from config import CHAT_ID_TG

FLAG = False


async def begin_send_messages(message: types.Message):
    global FLAG
    FLAG = True
    await message.answer('Режим оповещения включен')
    while True:
        if not FLAG:
            return
        day_now = datetime.date.today()
        time_now = datetime.datetime.now()
        messages = get_sent_message(day_now.strftime('%d.%m.%y'), time_now.strftime('%H:%M'))
        if messages:
            for row in messages:
                if row[3] == 'преподавательский':
                    await message.bot.send_message(CHAT_ID_TG, row[1])
                    if row[2] == 'ежедневно':
                        new_near_data = day_now + datetime.timedelta(days=1)
                    elif row[2] == 'еженедельно':
                        new_near_data = day_now + datetime.timedelta(weeks=1)
                    else:
                        try:
                            new_near_data = day_now.replace(month=day_now.month + 1)
                        except ValueError:
                            new_near_data = day_now.replace(month=day_now.month + 1, day=28)
                    change_near_date(row[0], new_near_data.strftime('%d.%m.%y'))
        await asyncio.sleep(55)


async def stop_send_messages(message: types.Message):
    global FLAG
    FLAG = False
    await message.answer('Режим оповещения отключен')
    return


def register_send_messages(dp: Dispatcher):
    dp.register_message_handler(begin_send_messages, commands=['start_notifier'], state=['*'])
    dp.register_message_handler(stop_send_messages, commands=['stop_notifier'], state=['*'])
    dp.register_message_handler(begin_send_messages, Text(equals='включить рассылку', ignore_case=True),
                                state=Notifier.waiting_work_with_notifier)
    dp.register_message_handler(stop_send_messages, Text(equals='остановить рассылку', ignore_case=True),
                                state=Notifier.waiting_work_with_notifier)




