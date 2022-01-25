import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


from config import TOKEN_API
from utils.comon import register_common
from apps.notifier.handlers.make_message import register_make_messages
from apps.notifier.handlers.send_message import register_send_messages
from apps.notifier.handlers.main_menu import register_module_notifier


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.setup_middleware(LoggingMiddleware())

register_common(dp)
register_make_messages(dp)
register_send_messages(dp)
register_module_notifier(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
