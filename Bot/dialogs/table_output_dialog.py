"""
A dialogue in which the user
the diary is sent in excel form
tables in message
"""

import logging

from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Button
from aiogram_dialog.widgets.text import Format

from databases.database import session_maker
from databases.orm_query import orm_get_user_data
from dialogs.common_windows import WindowNoRows
from dialogs.getters.getters import get_number_rows_userdata
from states.states import TableOutputSG
from utils.output_table import save_data_excel

logger = logging.getLogger(__name__)


async def get_diary(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    data = await orm_get_user_data(
        session_maker, int(dialog_manager.event.from_user.id)
    )

    save_data_excel(data, int(dialog_manager.event.from_user.id))

    doc = FSInputFile(f"./tables/{int(dialog_manager.event.from_user.id)}.xlsx")

    await callback.message.answer_document(doc)


table_output_dialog = Dialog(
    WindowNoRows(
        state=TableOutputSG.zero,
        getter=get_number_rows_userdata,
        txt="{next_cancel_table}",
        when_1="rows_yes",
        when_2="rows_no",
    ),
    Window(
        Format(
            text="{receive_diary}",
            when="rows_yes",
        ),
        Format(
            text="{no_entry}",
            when="rows_no",
        ),
        Cancel(Format(text="{start}"), when="rows_no"),
        Cancel(
            Format("{get_table}"),
            id="but_get_table",
            on_click=get_diary,
            when="rows_yes",
        ),
        Cancel(Format("{but_cancel}"), when="rows_yes"),
        state=TableOutputSG.first,
        getter=get_number_rows_userdata,
    ),
)
