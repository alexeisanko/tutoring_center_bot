from aiogram.dispatcher.filters.state import State, StatesGroup


class MakeAdmin(StatesGroup):
    waiting_for_login = State()
    waiting_for_password = State()
