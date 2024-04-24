from dataclasses import dataclass

from config.config import Database, RedisConfig, TgBot, Email
from config.config_data import DEVELOPMENT

if DEVELOPMENT:
    from config.config_data import (
        data_database_dev,
        data_redis_dev,
        data_bot_dev,
        data_email_dev,
    )

    data_db = data_database_dev
    data_redis = data_redis_dev
    data_bot = data_bot_dev
    data_email = data_email_dev
else:
    from config.config_data import data_database, data_redis, data_bot, data_email

    data_db = data_database
    data_redis = data_redis
    data_bot = data_bot
    data_email = data_email


@dataclass
class Config:
    database: Database
    tg_bot: TgBot
    email_config: Email
    redis_config: RedisConfig


config = Config(
    database=Database(data_db),
    tg_bot=TgBot(data_bot),
    email_config=Email(data_email),
    redis_config=RedisConfig(data_redis),
)

DB_URL = (
    f"postgresql+asyncpg://{config.database.data['DB_USER']}:{config.database.data['DB_PASS']}@"
    f"{config.database.data['DB_HOST']}/{config.database.data['DB_NAME']}"
)
