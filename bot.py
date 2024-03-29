import logging

from vkbottle.bot import Bot as BotVK
from config import TOKEN_API_VK
from apps.reg_for_trial_exam.google_api import drive
import apps
import vk_utils


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s')


# def bot_tg():
#     bot = BotTG(token=TOKEN_API_TG)
#     dp = Dispatcher(bot, storage=MemoryStorage())
#     dp.setup_middleware(LoggingMiddleware())
#     register_common(dp)
#     register_notifier(dp)
#     register_reg_user(dp)
#     executor.start_polling(dp, skip_updates=True)


def bot_vk():
    drive.CURRENT_SHEETS_ID = drive.make_current_workbook()
    bot = BotVK(token=TOKEN_API_VK)

    for bp in vk_utils.bps:
        bp.load(bot)

    for bp in apps.bps:
        bp.load(bot)

    bot.run_forever()


if __name__ == '__main__':
    bot_vk()
