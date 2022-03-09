from vkbottle.bot import Blueprint
from vkbottle.bot import Message
import datetime
import asyncio
import random

from config import CHAT_ID_VK
from apps.notifier.models import get_sent_message, change_near_date

bp = Blueprint()
FLAG_GENERAL = False
FLAG_PRIVATE = False


@bp.on.private_message(command='start_mailing')
async def begin_send_message(message: Message):
    global FLAG_GENERAL
    FLAG_GENERAL = True
    await message.answer('Режим оповещения включен')
    while True:
        if not FLAG_GENERAL:
            return
        day_now = datetime.date.today()
        time_now = datetime.datetime.now()
        messages = get_sent_message(day_now.strftime('%d.%m.%y'), time_now.strftime('%H:%M'))
        if messages:
            for row in messages:
                if row[3] == 'ученический':
                    await bp.api.messages.send(chat_id=CHAT_ID_VK, random_id=random.randint(1, 100000), message=row[1])
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


@bp.on.private_message(command='stop_mailing')
async def stop_send_messages(message: Message):
    global FLAG_GENERAL
    FLAG_GENERAL = False
    await message.answer('Режим оповещения отключен')
    return



