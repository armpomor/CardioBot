import logging
from typing import TYPE_CHECKING

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import ManagedTextInput
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Cancel
from aiogram_dialog.widgets.text import Format
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

from databases.database import session_maker
from databases.orm_query import orm_update_user
from dialogs.common_windows import WindowFinished, WindowInputEmail
from dialogs.getters.getters import get_email
from states.states import EmailSG

logger = logging.getLogger(__name__)


async def incorrect_email(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    await message.answer(text=f"{i18n.incorrect_input()}\n{i18n.cancel_input()}")


async def save_email(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    data = await get_email(dialog_manager, i18n)

    await orm_update_user(
        session_maker, {"email": data["email"]}, int(dialog_manager.event.from_user.id)
    )


async def next_step(event, widget, dialog_manager: DialogManager, *_) -> None:
    await dialog_manager.switch_to(EmailSG.save)


email_dialog = Dialog(
    WindowInputEmail(state=EmailSG.first, success=next_step, error=incorrect_email),
    Window(
        Format(text="{save_cancel_email}"),
        SwitchTo(
            text=Format("{save}"),
            id="save_data_button",
            on_click=save_email,
            state=EmailSG.finished,
        ),
        Cancel(Format("{but_cancel}"), id="but_cancel"),
        state=EmailSG.save,
        getter=get_email,
    ),
    WindowFinished(state=EmailSG.finished, txt="{save_email}"),
)
