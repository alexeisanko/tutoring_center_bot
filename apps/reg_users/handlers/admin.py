from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext


from config import ADMIN_LOGIN, ADMIN_PASSWORD
from apps.reg_users.state import MakeAdmin
from apps.reg_users.models import save_admin_user
from tg_utils.common_handlers import start_keyboard


async def register(message: types.Message):
    await message.answer('Введите логин')
    await MakeAdmin.waiting_for_login.set()


async def add_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text.lower())
    await MakeAdmin.next()
    await message.answer('Введите пароль')


async def add_password(message: types.Message, state: FSMContext):
    login = await state.get_data()
    if login['login'] == ADMIN_LOGIN and message.text.lower() == ADMIN_PASSWORD:
        save_admin_user(message.from_user.id)
        await state.finish()
        await message.answer(f'Привет {message.from_user.username}! Ты есть в списках, теперь можно поработать.',
                             reply_markup=start_keyboard())
    else:
        await state.finish()
        await message.answer('Неверный пароль или логин. можете попробывать еще раз /registration\n'
                             'Либо можешь пользоваться модулями доступными для любого пользователя',
                             reply_markup=start_keyboard())


def register_new_admin(dp: Dispatcher):
    dp.register_message_handler(register, commands=['registration'], state=['*'])
    dp.register_message_handler(add_login, state=MakeAdmin.waiting_for_login)
    dp.register_message_handler(add_password, state=MakeAdmin.waiting_for_password)
