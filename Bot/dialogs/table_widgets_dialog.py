"""
Dialogue in which the user's request
the diary is returned (last 21 lines)
in the form of widgets with the ability to edit
records.
"""

import logging
import operator
from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog.widgets.kbd import (
    Cancel,
    Button,
    Column,
    Multiselect,
    SwitchTo,
    Next,
    Radio,
)
from aiogram_dialog.widgets.text import Format

from databases.database import session_maker
from databases.orm_query import (
    orm_delete_row_user_data,
)
from dialogs.common_windows import WindowNoRows, WindowFinished
from dialogs.entry_dialog import incorrect_entry, incorrect_comment, save_data
from dialogs.getters.getters import (
    get_number_rows_userdata,
    result_getter,
    get_data,
    get_row,
    get_texts_dialogs,
)
from states.states import TableWidgetsSG
from utils.data_checking import (
    check_systolic,
    check_diastolic,
    check_pulse,
    check_comment,
)

logger = logging.getLogger(__name__)


async def delete_row(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    """
    Handler in which we delete one record
    from the user, finding it by str(datetime)
    """
    user_id = int(dialog_manager.event.from_user.id)
    date_time = dialog_manager.find("row").get_checked()

    await orm_delete_row_user_data(
        session_maker, user_id, datetime.strptime(date_time[0], "%Y-%m-%d %H:%M")
    )


async def update_date(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    """
    Handler in which we first delete the string being modified
    from the database, and then save the newly entered one with the old
    """
    user_id = int(dialog_manager.event.from_user.id)
    date_time = dialog_manager.dialog_data.get("date_time")

    await orm_delete_row_user_data(session_maker, user_id, date_time)

    await save_data(callback, button, dialog_manager)


CANCEL_EDIT_DATA = SwitchTo(
    Format("{cancel_edit}"), id="cancel", state=TableWidgetsSG.first
)


table_widgets_dialog = Dialog(
    WindowNoRows(
        state=TableWidgetsSG.zero,
        getter=get_number_rows_userdata,
        txt="{next_cancel_display_entry}",
        when_1="rows_yes",
        when_2="rows_no",
    ),
    Window(
        Format(text="{mark_row}"),
        Column(
            Multiselect(
                checked_text=Format(
                    "[✔️]{item[0]} - {item[1]}/{item[2]} - pulse: {item[3]}".ljust(150)
                ),
                unchecked_text=Format(
                    "[  ]{item[0]} - {item[1]}/{item[2]} - pulse: {item[3]}".ljust(150)
                ),
                id="row",
                item_id_getter=operator.itemgetter(0),
                items="rows",
                max_selected=1,
                min_selected=0,
            ),
        ),
        Format(text="{delete_edit_row}", when="result"),
        SwitchTo(
            Format(text="{delete_row}"),
            id="delete_row",
            on_click=delete_row,
            state=TableWidgetsSG.delete,
            when="result",
        ),
        SwitchTo(
            Format(text="{edit_row}"),
            id="edit_row",
            when="result",
            state=TableWidgetsSG.systolic,
        ),
        Cancel(
            Format("{but_cancel}"),
            when="result",
        ),
        state=TableWidgetsSG.first,
        getter=get_data,
    ),
    Window(
        Format("{row_delete}"),
        Cancel(Format("Старт")),
        state=TableWidgetsSG.delete,
        getter=get_texts_dialogs,
    ),
    Window(
        Format("{edit_systolic}"),
        TextInput(
            id="systolic",
            type_factory=check_systolic,
            on_success=Next(),
            on_error=incorrect_entry,
        ),
        CANCEL_EDIT_DATA,
        state=TableWidgetsSG.systolic,
        getter=get_row,
    ),
    Window(
        Format("{edit_diastolic}"),
        TextInput(
            id="diastolic",
            type_factory=check_diastolic,
            on_success=Next(),
            on_error=incorrect_entry,
        ),
        CANCEL_EDIT_DATA,
        state=TableWidgetsSG.diastolic,
        getter=get_row,
    ),
    Window(
        Format("{edit_pulse}"),
        TextInput(
            id="pulse",
            type_factory=check_pulse,
            on_success=Next(),
            on_error=incorrect_entry,
        ),
        CANCEL_EDIT_DATA,
        state=TableWidgetsSG.pulse,
        getter=get_row,
    ),
    Window(
        Format("{edit_arrhythmia}"),
        Radio(
            checked_text=Format("🔘 {item}"),
            unchecked_text=Format("⚪️ {item}"),
            id="arrhythmia",
            item_id_getter=lambda x: x,
            items="question_arrhythmia",
            on_click=Next(),
        ),
        CANCEL_EDIT_DATA,
        state=TableWidgetsSG.arrhythmia,
        getter=get_row,
    ),
    Window(
        Format("{edit_comment}"),
        TextInput(
            id="comment",
            on_success=Next(),
            type_factory=check_comment,
            on_error=incorrect_comment,
        ),
        CANCEL_EDIT_DATA,
        state=TableWidgetsSG.comment,
        getter=get_row,
    ),
    Window(
        Format(
            "<u>{texts_dialog[you_entered]}</u>\n\n"
            "<b>{texts_dialog[systolic_press]}</b>: {result_data[systolic]}\n"
            "<b>{texts_dialog[diastolic_press]}</b>: {result_data[diastolic]}\n"
            "<b>{texts_dialog[pulse]}</b>: {result_data[pulse]}\n"
            "<b>{texts_dialog[arrhythmia]}</b>: {result_data[arrhythmia]}\n"
            "<b>{texts_dialog[comment]}</b>: {result_data[comment]}\n"
        ),
        CANCEL_EDIT_DATA,
        SwitchTo(
            Format("{texts_dialog[save_data]}"),
            state=TableWidgetsSG.save_data,
            on_click=update_date,
            id="save_data",
        ),
        state=TableWidgetsSG.update_data,
        getter=result_getter,
        parse_mode="html",
    ),
    WindowFinished(state=TableWidgetsSG.save_data, txt="{update_save}"),
)
