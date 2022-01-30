import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import TOKEN_API_TG
from utils.comon import register_common
from apps.notifier.manage import register_notifier

from vkbottle.bot import Bot
from config import TOKEN_API_VK
from apps.notifier.handlers.send_messages_vk import bp

from multiprocessing import Process

logging.basicConfig(level=logging.INFO)


def bot_vk():
    bot = Bot(token=TOKEN_API_VK)
    bp.load(bot)
    bot.run_forever()


def bot_tg():
    bot = Bot(token=TOKEN_API_TG)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.setup_middleware(LoggingMiddleware())

    register_common(dp)
    register_notifier(dp)
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    tg = Process(target=bot_tg)
    vk = Process(target=bot_tg)
    tg.start()
    vk.start()
    tg.join()
    vk.join()
