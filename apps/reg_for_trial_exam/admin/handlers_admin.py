import random

from vkbottle.bot import Blueprint, Message
from vkbottle import Keyboard, Text, KeyboardButtonColor
from vkbottle import VKAPIError
from ..state import AdminState
from ..google_api import sheets
from config import MESSAGES, ADMIN_ID, GROUP_VK_ID

bp = Blueprint()
STORAGE = {}


def admin_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("Отправить информационное сообщение"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("Изменить текстовку"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("Запустить регистрацию"), color=KeyboardButtonColor.POSITIVE)
    keyboard.row()
    keyboard.add(Text("Остановить регистрацию"), color=KeyboardButtonColor.NEGATIVE)
    keyboard.row()
    keyboard.add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE).get_json()
    return keyboard.get_json()


def cansel_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE).get_json()
    return keyboard


@bp.on.private_message(text='admin')
async def start_admin(message: Message):
    if message.peer_id in ADMIN_ID:
        await message.answer("Приветствую вас Юлия. Чем могу быть полезен?", keyboard=admin_keyboard())

    else:
        await message.answer('Отказ в доступе')
    await bp.state_dispenser.delete(message.peer_id)


@bp.on.private_message(text='Отправить информационное сообщение')
async def write_message(message: Message):
    await message.answer("Напиши текст и мы в точности его повторим всем учатсникам группы", keyboard=cansel_keyboard())
    await bp.state_dispenser.set(message.peer_id, AdminState.WRITE_MESSAGE)


@bp.on.private_message(state=AdminState.WRITE_MESSAGE)
async def send_message(message: Message):
    writer_message = message.text
    members = dict(await bp.api.groups.get_members(GROUP_VK_ID))
    for member in members['items']:
        try:
            await bp.api.messages.send(message=writer_message,
                                       user_id=member,
                                       random_id=random.randint(1, 1000000))
        except VKAPIError:
            continue
    await message.answer("Повторил всем в точности как ты хотела")
    await bp.state_dispenser.delete(message.peer_id)


def change_text_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    for i, msg in enumerate(MESSAGES.keys()):
        if i % 2 == 0:
            keyboard.add(Text(msg), color=KeyboardButtonColor.POSITIVE)
        else:
            keyboard.add(Text(msg), color=KeyboardButtonColor.POSITIVE)
            keyboard.row()
    keyboard.add(Text("Отмена"), color=KeyboardButtonColor.NEGATIVE)
    return keyboard.get_json()


@bp.on.private_message(text='Изменить текстовку')
async def choice_text(message: Message):
    await message.answer("Выбирай текст который будем менять", keyboard=change_text_keyboard())
    await bp.state_dispenser.set(message.peer_id, AdminState.CHOICE_TEXT)


@bp.on.private_message(state=AdminState.CHOICE_TEXT)
async def write_text(message: Message):
    msg = message.text
    STORAGE['msg'] = msg
    await message.answer(f"Хорошо, напиши как надо и мы все поменяем \n\n Если что, сейчас текст такой: \n\n\n {MESSAGES[msg]}",  keyboard=cansel_keyboard())
    await bp.state_dispenser.set(message.peer_id, AdminState.CHANGE_TEXT)


@bp.on.private_message(state=AdminState.CHANGE_TEXT)
async def change_text(message: Message):
    MESSAGES[STORAGE['msg']] = message.text
    await message.answer("Поменяли слово в слово")
    await bp.state_dispenser.delete(message.peer_id)
