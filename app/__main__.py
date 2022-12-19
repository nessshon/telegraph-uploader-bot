from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from aiogram.utils.exceptions import Unauthorized
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from environs import Env


def init():
    from . import logging
    logging.setup()

    env = Env()
    env.read_env()

    bot = Bot(token=env.str("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher(bot=bot, storage=MemoryStorage())

    try:
        from . import main

        executor.start_polling(
            dispatcher=dp,
            skip_updates=False,
            reset_webhook=True,
            on_startup=main.on_startup,
            on_shutdown=main.on_shutdown,
        )
    except Unauthorized:
        logging.logger.error("Invalid bot token!")

    except Exception as e:
        logging.logger.error(e)


if __name__ == "__main__":
    init()
