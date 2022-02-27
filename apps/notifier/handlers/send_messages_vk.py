from vkbottle.bot import Blueprint
from vkbottle.bot import Message
import datetime
import asyncio
import random

from config import CHAT_ID_VK
from apps.notifier.models import get_sent_message, change_near_date
from vk_utils.common_handlers import start_keyboard

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


@bp.on.private_message(command='start_private_mailing')
async def begin_send_private_message(message: Message):
    global FLAG_PRIVATE
    FLAG_PRIVATE = True
    await message.answer('Режим оповещения в личку включен')
    while True:
        if not FLAG_PRIVATE:
            return
        if datetime.datetime.now().weekday() == 1 and datetime.datetime.now().hour == 12:
            members = dict(await bp.api.groups.get_members(205480957))
            for member in members['items']:
                await bp.api.messages.send(message='Привет!\n'
                                                   'Желаю тебе хорошей учебной недели! '
                                                   'Открыта регистрация на пробник, может сразу запишемся?\n\n'
                                                   'P.S. Напоминаю, что делайн для записи - пятница 14:00. '
                                                   'После этого запись прекращается',
                                           user_id=member,
                                           random_id=random.randint(1, 1000000), keyboard=start_keyboard())
        elif datetime.datetime.now().weekday() == 3 and datetime.datetime.now().hour == 12:
            members = dict(await bp.api.groups.get_members(205480957))
            for member in members['items']:
                await bp.api.messages.send(message='Салют!\n'
                                                   'Завтра последний день для записи на пробный экзамен, ты уже '
                                                   'записался?\n\n '
                                                   'P.S. Напоминаю, что делайн для записи - пятница 14:00. После '
                                                   'этого запись прекращается',
                                           user_id=member,
                                           random_id=random.randint(1, 1000000))
        await asyncio.sleep(60)


@bp.on.private_message(command='stop_private_mailing')
async def stop_send_private_messages(message: Message):
    global FLAG_PRIVATE
    FLAG_PRIVATE = False
    await message.answer('Режим оповещения в личку отключен')
    return
