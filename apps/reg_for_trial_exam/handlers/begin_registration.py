from vkbottle.bot import Blueprint
from vkbottle.bot import Message
from vkbottle import VKAPIError
import datetime
import asyncio
import random

from vk_utils.common_handlers import start_keyboard
from config import GROUP_VK_ID, MESSAGES, ADMIN_ID
from ..google_api import drive

bp = Blueprint()

FLAG_PRIVATE = False


@bp.on.private_message(text='Запустить регистрацию')
@bp.on.private_message(command='start_reg_to_exam')
async def begin_send_private_message(message: Message):
    if message.peer_id in ADMIN_ID:
        global FLAG_PRIVATE
        FLAG_PRIVATE = True
        await message.answer('Режим регистрации на пробный экзамен включен')
        while True:
            if not FLAG_PRIVATE:
                return
            if datetime.datetime.now().weekday() == 0 and datetime.datetime.now().hour == 9:
                drive.copy_to_archive()
                drive.CURRENT_SHEETS_ID = drive.make_current_workbook()
                members = dict(await bp.api.groups.get_members(GROUP_VK_ID))
                for member in members['items']:
                    try:
                        await bp.api.messages.send(message=MESSAGES['Начало записи'],
                                                   user_id=member,
                                                   random_id=random.randint(1, 1000000), keyboard=start_keyboard())
                    except VKAPIError:
                        continue
            elif datetime.datetime.now().weekday() == 2 and datetime.datetime.now().hour == 9:
                members = dict(await bp.api.groups.get_members(GROUP_VK_ID))
                for member in members['items']:
                    try:
                        await bp.api.messages.send(message=MESSAGES['Напоминание про запись в среду'],
                                                   user_id=member,
                                                   random_id=random.randint(1, 1000000))
                    except VKAPIError:
                        continue
            await asyncio.sleep(3600)


@bp.on.private_message(text='Остановить регистрацию')
@bp.on.private_message(command='stop_reg_to_exam')
async def stop_send_private_messages(message: Message):
    if message.peer_id in ADMIN_ID:
        global FLAG_PRIVATE
        FLAG_PRIVATE = False
        await message.answer('Режим регистрации останавливается в течении часа!! \n прошу следующий запуск осуществлять не менее чем через час!'
                             'Если нужно более быстро отключать скажите, исправим.')
        return


@bp.on.private_message(command='new')
async def begin_send_private_message(message: Message):
    drive.CURRENT_SHEETS_ID = drive.make_current_workbook()
    print(drive.CURRENT_SHEETS_ID)


@bp.on.private_message(command='old')
async def begin_send_private_message(message: Message):
    drive.copy_to_archive()
    print(drive.CURRENT_SHEETS_ID)
