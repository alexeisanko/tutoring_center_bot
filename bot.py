import logging
from aiogram import Bot as BotTG, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from config import TOKEN_API_TG
from utils.comon import register_common
from apps.notifier.manage import register_notifier
from apps.reg_users import register_reg_user

from vkbottle.bot import Bot as BotVK
from config import TOKEN_API_VK
from apps.notifier.handlers.send_messages_vk import bp

from multiprocessing import Process

logging.basicConfig(level=logging.INFO)


def bot_tg():
    bot = BotTG(token=TOKEN_API_TG)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.setup_middleware(LoggingMiddleware())

    register_common(dp)
    register_notifier(dp)
    register_reg_user(dp)
    executor.start_polling(dp, skip_updates=True)


def bot_vk():
    bot = BotVK(token=TOKEN_API_VK)
    bp.load(bot)
    bot.run_forever()


if __name__ == '__main__':
    tg = Process(target=bot_tg)
    vk = Process(target=bot_vk)
    tg.start()
    vk.start()
    tg.join()
    vk.join()
