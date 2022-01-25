import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


from config import TOKEN_API
from utils.comon import register_common
from apps.notifier.manage import register_notifier


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN_API)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.setup_middleware(LoggingMiddleware())

register_common(dp)
register_notifier(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
