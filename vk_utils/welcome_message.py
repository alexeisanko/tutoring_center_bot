import random
from vkbottle.bot import Blueprint
from vk_utils.common_handlers import start_keyboard
from config import GROUP_VK_ID
from vkbottle import VKAPIError

bp = Blueprint()


async def send_welcome_message():
    members = dict(await bp.api.groups.get_members(GROUP_VK_ID))
    for member in members['items']:
        try:
            await bp.api.messages.send(message='Привет!\n'
                                               'Желаю тебе хорошей учебной недели! '
                                               'Открыта регистрация на пробник, может сразу запишемся?\n\n'
                                               'P.S. Напоминаю, что делайн для записи - четверг 20:00. '
                                               'После этого запись прекращается',
                                       user_id=member,
                                       random_id=random.randint(1, 1000000), keyboard=start_keyboard())
        except VKAPIError:
            continue
