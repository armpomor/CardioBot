from typing import Callable, Any, Dict, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from cachetools import TTLCache

from config.get_settings import config


class ThrottlingMiddleware(BaseMiddleware):
    """
    Middleware for throttling
    """

    def __init__(self, rate_limit: float = config.tg_bot.data["RATE_LIMIT"]) -> None:
        self.cache = TTLCache(maxsize=10000, ttl=rate_limit)

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        if user_id in self.cache:
            return

        self.cache[user_id] = True

        return await handler(event, data)
