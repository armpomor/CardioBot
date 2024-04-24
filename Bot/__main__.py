import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, DefaultKeyBuilder
from aiogram_dialog import setup_dialogs
from fluentogram import TranslatorHub
from redis.asyncio.client import Redis

from config.get_settings import config
from databases.database import create_db, drop_db
from dialogs import get_dialogs
from handlers import get_handlers
from middlewares import register_middlewares
from utils.i18n import create_translator_hub

logger = logging.getLogger(__name__)


async def on_startup(bot: Bot) -> None:
    if config.tg_bot.data["RUN_PARAM"]:
        await drop_db()

    await create_db()


async def on_shutdown(bot: Bot) -> None:
    logging.info("Bot is shutting down")


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="\033[92m{filename}:{funcName}:{lineno} - {message}",
        style="{",
    )

    bot = Bot(
        token=config.tg_bot.data["TOKEN"],
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )

    if config.tg_bot.data["USE_REDIS"]:
        redis = Redis(
            host=config.redis_config.data["REDIS_HOST"],
            port=config.redis_config.data["REDIS_PORT"],
            db=1,
        )
        storage = RedisStorage(
            redis=redis,
            key_builder=DefaultKeyBuilder(with_destiny=True, with_bot_id=True),
        )
    else:
        storage = MemoryStorage()

    dp = Dispatcher(
        storage=storage, maintenance_mode=config.tg_bot.data["MAINTENANCE_MODE"]
    )

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    # Создаем объект типа TranslatorHub
    translator_hub: TranslatorHub = create_translator_hub()

    register_middlewares(dp)

    #  Регистрируем роутеры и диалоги
    dp.include_routers(
        get_handlers(),
        get_dialogs(),
    )
    setup_dialogs(dp)

    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == "__main__":
    asyncio.run(main())
