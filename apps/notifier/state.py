from aiogram.dispatcher.filters.state import State, StatesGroup


class MakeMessage(StatesGroup):
    waiting_for_text = State()
    waiting_for_check_text = State()
    waiting_how_often_repeat_text = State()
    waiting_day_of_the_week = State()
    waiting_time = State()
    waiting_type_chat = State()


class Notifier(StatesGroup):
    waiting_work_with_notifier = State()


class ShowMessage(StatesGroup):
    waiting_choice_message = State()


class ChangeMessage(StatesGroup):
    waiting_choice_message = State()
    waiting_choice_change = State()
    waiting_add_change = State()
    waiting_save_change = State()


class DeleteMessage(StatesGroup):
    waiting_choice_message = State()
    waiting_accept_delete = State()
