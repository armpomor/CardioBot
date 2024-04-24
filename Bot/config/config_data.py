from os import getenv

from environs import Env

env = Env()
env.read_env()

DEVELOPMENT = False
BANNED = []  # List of banned users
FINISHED = "finished"

"""
MODE - if True, then the bot will work in maintenance mode
MAINTENANCE_MODE - if False, then the bot will work in maintenance mode
RUN_PARAM - if True, then all tables in the database will be deleted
RATE_LIMIT - key lifetime in cache during throttling
"""
data_common_bot = {
    "MODE": False,
    "MAINTENANCE_MODE": True,
    "RUN_PARAM": False,
    "RATE_LIMIT": 1.0,
    "USE_REDIS": False,
}

if DEVELOPMENT:
    data_database_dev = {
        "DB_NAME": env("DB_NAME"),
        "DB_USER": env("DB_USER"),
        "DB_PASS": env("DB_PASS"),
        "DB_HOST": env("DB_HOST"),
        "DB_PORT": env("DB_PORT"),
    }
    data_redis_dev = {
        "REDIS_HOST": env("REDIS_HOST"),
        "REDIS_PORT": env("REDIS_PORT"),
        "REDIS_DB": env("REDIS_DB"),
        "REDIS_PASS": env("REDIS_PASS"),
    }
    data_bot_dev = {
        "TOKEN": env("TOKEN"),
        "ADMIN_ID": env("ADMIN_ID"),
    } | data_common_bot
    data_email_dev = {
        "EMAIL": env("EMAIL"),
        "EMAIL_PASS": env("EMAIL_PASS"),
    }

data_database = {
    "DB_NAME": getenv("DB_NAME"),
    "DB_USER": getenv("DB_USER"),
    "DB_PASS": getenv("DB_PASS"),
    "DB_HOST": getenv("DB_HOST"),
    "DB_PORT": getenv("DB_PORT"),
}
data_redis = {
    "REDIS_HOST": getenv("REDIS_HOST"),
    "REDIS_PORT": getenv("REDIS_PORT"),
    "REDIS_DB": getenv("REDIS_DB"),
    "REDIS_PASS": getenv("REDIS_PASS"),
}
data_bot = {"TOKEN": getenv("TOKEN"), "ADMIN_ID": getenv("ADMIN_ID")} | data_common_bot
data_email = {
    "EMAIL": getenv("EMAIL"),
    "EMAIL_PASS": getenv("EMAIL_PASS"),
}
