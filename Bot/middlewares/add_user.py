import logging
from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from databases.database import session_maker
from databases.orm_query import orm_add_user

logger = logging.getLogger(__name__)


class AddUserMiddleware(BaseMiddleware):
    """
    Adds a new user to the database
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data_temp = dict()
        data_temp["user_id"] = event.from_user.id
        data_temp["name"] = event.from_user.first_name
        data_temp["language_code"] = event.from_user.language_code

        await orm_add_user(session_maker, data_temp)

        return await handler(event, data)
