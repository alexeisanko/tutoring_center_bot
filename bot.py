import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware


from config import TOKEN_API
from utils.comon import register_common
from apps.notifier.handlers.make_message import register_work_with_messages


async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=TOKEN_API)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.setup_middleware(LoggingMiddleware())

    register_common(dp)
    register_work_with_messages(dp)

    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())





