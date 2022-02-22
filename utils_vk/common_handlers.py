from vkbottle.bot import Blueprint
from vkbottle.bot import Message
from vkbottle import Keyboard, Text, KeyboardButtonColor

bp = Blueprint()


def start_keyboard():
    keyboard = Keyboard(one_time=True, inline=False)
    keyboard.add(Text("Записаться на пробный экз."), color=KeyboardButtonColor.POSITIVE).get_json()
    return keyboard


@bp.on.private_message(command='start')
async def start(message: Message):
    await message.answer('Привет!\n'
                         'Я - чат-робот учебного центра НьюСкул.\n'
                         'Пиши мне, если хочешь записаться на пробный экзамен!\n\n'
                         'P.S. Не забывай, что дедлайн по записи на пробники - 14:00 в пятницу. '
                         'После этого я уже не смогу тебя записать.', keyboard=start_keyboard())


