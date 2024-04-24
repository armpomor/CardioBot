import logging
import operator

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import (
    Column,
    Radio,
    ManagedRadio,
    Cancel,
    SwitchTo,
    Button,
)
from aiogram_dialog.widgets.text import Format

from databases.database import session_maker
from databases.orm_query import orm_update_user
from dialogs.common_windows import WindowFinished
from dialogs.getters.getters import get_timezone
from states.states import TimezoneSG

logger = logging.getLogger(__name__)


async def save_timezone(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    timezone = dialog_manager.find("timezone").get_checked()

    await orm_update_user(
        session_maker,
        {"timezone": int(timezone)},
        int(dialog_manager.event.from_user.id),
    )


async def next_step(
    callback: CallbackQuery,
    radio: ManagedRadio,
    dialog_manager: DialogManager,
    *args,
    **kwargs,
) -> None:
    await dialog_manager.switch_to(TimezoneSG.save)


timezone_dialog = Dialog(
    Window(
        Format(text="{select_timezone}"),
        Column(
            Radio(
                checked_text=Format("🔘 {item[0]}".ljust(150)),
                unchecked_text=Format("⚪️ {item[0]}".ljust(150)),
                id="timezone",
                item_id_getter=operator.itemgetter(1),
                items="tz",
                on_state_changed=next_step,
            ),
        ),
        Cancel(Format("{cancel_input}"), id="but_edit"),
        state=TimezoneSG.first,
        getter=get_timezone,
    ),
    Window(
        Format(text="{save_cancel_timezone}"),
        SwitchTo(
            text=Format("{save}"),
            id="save_data_button",
            on_click=save_timezone,
            state=TimezoneSG.finished,
        ),
        Cancel(Format("{but_cancel}"), id="but_cancel"),
        state=TimezoneSG.save,
        getter=get_timezone,
    ),
    WindowFinished(state=TimezoneSG.finished, txt="{save_timezone}"),
)
