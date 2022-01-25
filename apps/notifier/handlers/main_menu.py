from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text


from apps.notifier.keyboards import start_keyboard
from apps.notifier.state import Notifier


async def module_notifier(message: types.Message):
    # admins_users = models.get_admin_users_id()
    # admins = []
    # for admin in admins_users:
    #     admins.append(admin[0])
    # if message.from_user.id not in admins:
    #     await message.answer('Недостаточный уровень доступа. Введите /registration для проверки.')
    #     return
    keyboard = start_keyboard()
    await Notifier.waiting_work_with_notifier.set()
    await message.answer('Модуль "Рассылка" открыт', reply_markup=keyboard)


def register_module_notifier(dp: Dispatcher):
    dp.register_message_handler(module_notifier, Text(equals='рассылка сообщений', ignore_case=True))