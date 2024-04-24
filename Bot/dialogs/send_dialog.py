import logging
from typing import TYPE_CHECKING

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Next, Cancel, Button, Start
from aiogram_dialog.widgets.text import Format
from fluentogram import TranslatorRunner
from yagmail import SMTP

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

from config.get_settings import config
from databases.database import session_maker
from databases.orm_query import orm_get_user_data
from dialogs.common_windows import WindowNoRows, WindowFinished
from dialogs.getters.getters import (
    get_number_rows_userdata,
    get_user_email,
)
from states.states import SendSG, EmailSG
from utils.output_table import save_data_excel

logger = logging.getLogger(__name__)


async def send_email(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    """
    Sending a letter with a diary
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    data = await orm_get_user_data(
        session_maker, int(dialog_manager.event.from_user.id)
    )

    email = dialog_manager.dialog_data.get("email")

    if email is None:
        email = dialog_manager.find("email").get_value()

    save_data_excel(data, int(dialog_manager.event.from_user.id))

    yad = SMTP(
        config.email_config.data["EMAIL"], config.email_config.data["EMAIL_PASS"]
    )
    contents = [i18n.text_email()]

    yad.send(
        email,
        "subject",
        contents,
        attachments=[f"./tables/{int(dialog_manager.event.from_user.id)}.xlsx"],
    )


send_dialog = Dialog(
    WindowNoRows(
        state=SendSG.zero,
        getter=get_number_rows_userdata,
        txt="{next_cancel_send_email}",
        when_1="rows_yes",
        when_2="rows_no",
    ),
    Window(
        Format(text="{question_send}", when="email_yes"),
        Next(Format("{send}"), when="email_yes", on_click=send_email, id="send_email"),
        Start(
            Format(text="{change_email}"),
            id="email",
            state=EmailSG.first,
            when="email_yes",
        ),
        Cancel(Format("{but_cancel}"), when="email_yes", id="no_send"),
        Format(
            "{no_email}",
            when="email_no",
        ),
        Cancel(Format("{start}"), when="email_no"),
        state=SendSG.first,
        getter=get_user_email,
    ),
    WindowFinished(state=SendSG.finished, txt="{send_diary}"),
)
