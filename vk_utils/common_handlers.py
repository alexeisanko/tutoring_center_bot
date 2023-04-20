import logging

from vkbottle.bot import Blueprint
from vkbottle.bot import Message
from vkbottle import Keyboard, Text, KeyboardButtonColor

bp = Blueprint()
bp.labeler.vbml_ignore_case = True


def start_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("Записаться на пробный экз."), color=KeyboardButtonColor.POSITIVE).get_json()
    return keyboard


@bp.on.private_message(text='Начать')
@bp.on.private_message(command='start')
async def start(message: Message):
    await message.answer('Привет!\n'
                         'Я - чат-робот учебного центра НьюСкул.\n'
                         'Пиши мне, если хочешь записаться на пробный экзамен!\n\n'
                         'P.S. Не забывай, что дедлайн по записи на пробники - 20:00 в четверг. '
                         'После этого я уже не смогу тебя записать.', keyboard=start_keyboard())
    try:
        await bp.state_dispenser.delete(message.peer_id)
    except KeyError:
        pass

@bp.on.private_message(text='Отмена')
async def start(message: Message):
    logging.info(f'{message.peer_id} прекратил своб запись')
    await message.answer('Видимо что-то пошло не так. Возврашаемся в основное меню.\n\n'
                         'Хотите записаться на экзамен? Жми на кнопку',
                         keyboard=start_keyboard())
    try:
        await bp.state_dispenser.delete(message.peer_id)
    except KeyError:
        pass
