
import random
from vkbottle.bot import Blueprint
from vk_utils.common_handlers import start_keyboard


bp = Blueprint()


async def get_all_members():
    return await bp.api.groups.get_members(205480957)


async def send_welcome_message():
    members = dict(await get_all_members())
    for member in members['items']:
        await bp.api.messages.send(message='Привет!\n'
                                   'Я - чат-робот учебного центра НьюСкул.\n'
                                   'Пиши мне, если хочешь записаться на пробный экзамен!\n\n'
                                   'P.S. Не забывай, что дедлайн по записи на пробники - 14:00 в пятницу. '
                                   'После этого я уже не смогу тебя записать.', user_id=member,
                                   random_id=random.randint(1, 1000000), keyboard=start_keyboard())
