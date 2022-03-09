from vkbottle.bot import Blueprint
from vkbottle.bot import Message
import datetime
import asyncio
import random

from vk_utils.common_handlers import start_keyboard
from config import GROUP_VK_ID

bp = Blueprint()

FLAG_PRIVATE = False


@bp.on.private_message(command='start_private_mailing')
async def begin_send_private_message(message: Message):
    global FLAG_PRIVATE
    FLAG_PRIVATE = True
    await message.answer('Режим оповещения в личку включен')
    while True:
        if not FLAG_PRIVATE:
            return
        if datetime.datetime.now().weekday() == 1 and datetime.datetime.now().hour == 12:
            members = dict(await bp.api.groups.get_members(GROUP_VK_ID))
            for member in members['items']:
                await bp.api.messages.send(message='Привет!\n'
                                                   'Желаю тебе хорошей учебной недели! '
                                                   'Открыта регистрация на пробник, может сразу запишемся?\n\n'
                                                   'P.S. Напоминаю, что делайн для записи - пятница 14:00. '
                                                   'После этого запись прекращается',
                                           user_id=member,
                                           random_id=random.randint(1, 1000000), keyboard=start_keyboard())
        elif datetime.datetime.now().weekday() == 3 and datetime.datetime.now().hour == 12:
            members = dict(await bp.api.groups.get_members(GROUP_VK_ID))
            for member in members['items']:
                await bp.api.messages.send(message='Салют!\n'
                                                   'Завтра последний день для записи на пробный экзамен, ты уже '
                                                   'записался?\n\n '
                                                   'P.S. Напоминаю, что делайн для записи - пятница 14:00. После '
                                                   'этого запись прекращается',
                                           user_id=member,
                                           random_id=random.randint(1, 1000000))
        await asyncio.sleep(3600)


@bp.on.private_message(command='stop_private_mailing')
async def stop_send_private_messages(message: Message):
    global FLAG_PRIVATE
    FLAG_PRIVATE = False
    await message.answer('Режим оповещения в личку отключен')
    return


@bp.on.private_message(command='new')
async def begin_send_private_message(message: Message):
    from ..google_api import drive
    drive.make_current_workbook()
    print(drive.CURRENT_SHEETS_ID)


@bp.on.private_message(command='old')
async def begin_send_private_message(message: Message):
    from ..google_api import drive
    drive.copy_to_archive()
    print(drive.CURRENT_SHEETS_ID)