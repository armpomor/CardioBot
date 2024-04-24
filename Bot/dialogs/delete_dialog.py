import logging
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Cancel, Row
from aiogram_dialog.widgets.text import Format
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

from databases.database import session_maker
from databases.orm_query import orm_delete_user_data
from dialogs.common_windows import WindowNoRows, WindowFinished
from dialogs.getters.getters import (
    get_user_id,
    get_number_rows_userdata,
)
from states.states import DeleteSG

logger = logging.getLogger(__name__)


async def delete_data(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    user_id = await get_user_id(dialog_manager, i18n)

    await orm_delete_user_data(session_maker, user_id["user_id"])


delete_dialog = Dialog(
    WindowNoRows(
        state=DeleteSG.zero,
        getter=get_number_rows_userdata,
        txt="{next_cancel_del_data}",
        when_1="rows_yes",
        when_2="rows_no",
    ),
    Window(
        Format(text="{quest_delete}"),
        Row(
            SwitchTo(
                text=Format("{delete}"),
                id="delete_yes",
                on_click=delete_data,
                state=DeleteSG.finished,
            ),
            Cancel(Format("{no_delete}"), id="delete_no"),
        ),
        state=DeleteSG.delete,
        getter=get_user_id,
    ),
    WindowFinished(state=DeleteSG.finished, txt="{confirm_delete}"),
)
