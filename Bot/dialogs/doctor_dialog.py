import logging

from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Next, Cancel
from aiogram_dialog.widgets.text import Format

from dialogs.common_windows import WindowNoRows, WindowFinished, WindowInputEmail
from dialogs.email_dialog import incorrect_email
from dialogs.getters.getters import (
    get_number_rows_userdata,
    get_email,
)
from dialogs.send_dialog import send_email
from states.states import DoctorSG

logger = logging.getLogger(__name__)


async def next_step(event, widget, dialog_manager: DialogManager, *_) -> None:
    await dialog_manager.switch_to(DoctorSG.second)


doctor_dialog = Dialog(
    WindowNoRows(
        state=DoctorSG.zero,
        getter=get_number_rows_userdata,
        txt="{next_cancel_send_email}",
        when_1="rows_yes",
        when_2="rows_no",
    ),
    WindowInputEmail(state=DoctorSG.first, success=next_step, error=incorrect_email),
    Window(
        Format(text="{send_cancel_diary}"),
        Next(
            Format("{send}"),
            id="send_button",
            on_click=send_email,
        ),
        Cancel(Format("{but_cancel}"), id="but_cancel"),
        state=DoctorSG.second,
        getter=get_email,
    ),
    WindowFinished(state=DoctorSG.finished, txt="{send_diary}"),
)
