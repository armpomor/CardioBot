import logging
from datetime import date, datetime
from typing import TYPE_CHECKING

from aiogram import F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, ManagedTextInput
from aiogram_dialog.widgets.kbd import (
    Next,
    SwitchTo,
    Radio,
    Button,
    Cancel,
    Calendar,
    Group,
)
from aiogram_dialog.widgets.text import Format
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

from config.config_data import FINISHED
from databases.database import session_maker
from databases.orm_query import orm_add_data_user
from dialogs.common_windows import WindowFinished
from dialogs.getters.getters import result_getter, get_texts_entry_dialog
from states.states import EntrySG
from utils.data_checking import (
    check_systolic,
    check_diastolic,
    check_pulse,
    check_comment,
)

logger = logging.getLogger(__name__)

# Dialog widget to cancel editing.
# Appears when dialog_data.get(FINISHED_KEY) == True.
CANCEL_EDIT = SwitchTo(
    Format("{edit_cancel}"),
    when=F["dialog_data"][FINISHED],
    id="cancel_edit",
    state=EntrySG.preview,
)
CANCEL = Cancel(Format("{entry_cancel}"), id="but_edit")


async def next_or_end(event, widget, dialog_manager: DialogManager, *_) -> None:
    """
    Handler for moving to the next window or to
    review the entered data before saving
    """
    if dialog_manager.dialog_data.get(FINISHED):
        await dialog_manager.switch_to(EntrySG.preview)
    else:
        await dialog_manager.next()


async def on_date_selected(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, selected_date: date
) -> None:
    """
    Record date selection handler.
    :param callback:
    :param widget:
    :param dialog_manager:
    :param selected_date:
    :return:
    """
    await dialog_manager.update({"date": selected_date})

    await dialog_manager.next()


async def on_time_selected(
    callback: CallbackQuery, widget, dialog_manager: DialogManager, data: str
) -> None:
    """
    Handler for selecting the recording hour.
    :param callback:
    :param widget:
    :param dialog_manager:
    :param data:
    :return:
    """
    await dialog_manager.update({"hour": data})
    date_temp = dialog_manager.dialog_data.get("date")
    hour = dialog_manager.dialog_data.get("hour")

    date_time = datetime(date_temp.year, date_temp.month, date_temp.day, int(hour), 0)

    await dialog_manager.update({"date_time": date_time})

    await dialog_manager.next()


async def save_data(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    """
    Handler for saving data in the database.
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")
    data = await result_getter(dialog_manager, i18n)

    await orm_add_data_user(session_maker, data["result_data"])


async def incorrect_entry(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    """
    Handler that will be triggered in case of incorrect input
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    await message.answer(text=f"{i18n.incorrect_input()}\n{i18n.cancel_input()}")


async def incorrect_comment(
    message: Message, widget: ManagedTextInput, dialog_manager: DialogManager, text: str
) -> None:
    """
    Handler that will trigger when
    The comment length is more than 50 characters.
    """
    i18n: TranslatorRunner = dialog_manager.middleware_data.get("i18n")

    await message.answer(text=f"{i18n.long_comment()}\n{i18n.cancel_input()}")


entry_dialog = Dialog(
    Window(
        Format(text="{date_selection}"),
        Calendar(
            id="date",
            on_click=on_date_selected,
        ),
        CANCEL,
        state=EntrySG.date,
        getter=get_texts_entry_dialog,
    ),
    Window(
        Format(text="{time_selection}"),
        Group(
            Radio(
                checked_text=Format("🔘 {item}"),
                unchecked_text=Format("⚪️ {item}"),
                id="time",
                item_id_getter=lambda x: x,
                items=[x for x in range(24)],
                on_click=on_time_selected,
            ),
            width=4,
        ),
        CANCEL,
        state=EntrySG.time,
        getter=get_texts_entry_dialog,
    ),
    Window(
        Format(text="{entry_systolic}"),
        TextInput(
            id="systolic",
            type_factory=check_systolic,
            on_success=next_or_end,
            on_error=incorrect_entry,
        ),
        CANCEL_EDIT,
        CANCEL,
        state=EntrySG.systolic,
        getter=get_texts_entry_dialog,
    ),
    Window(
        Format(text="{entry_diastolic}"),
        TextInput(
            id="diastolic",
            type_factory=check_diastolic,
            on_success=next_or_end,
            on_error=incorrect_entry,
        ),
        CANCEL_EDIT,
        CANCEL,
        state=EntrySG.diastolic,
        getter=get_texts_entry_dialog,
    ),
    Window(
        Format(text="{entry_pulse}"),
        TextInput(
            id="pulse",
            type_factory=check_pulse,
            on_success=next_or_end,
            on_error=incorrect_entry,
        ),
        CANCEL_EDIT,
        CANCEL,
        state=EntrySG.pulse,
        getter=get_texts_entry_dialog,
    ),
    Window(
        Format(text="{presence_arrhythmia}"),
        Radio(
            checked_text=Format("🔘 {item}"),
            unchecked_text=Format("⚪️ {item}"),
            id="arrhythmia",
            item_id_getter=lambda x: x,
            items="question_arrhythmia",
            on_click=Next(),
        ),
        CANCEL_EDIT,
        CANCEL,
        state=EntrySG.arrhythmia,
        getter=get_texts_entry_dialog,
    ),
    Window(
        Format(text="{write_comment}"),
        TextInput(
            id="comment",
            type_factory=check_comment,
            on_success=next_or_end,
            on_error=incorrect_comment,
        ),
        CANCEL_EDIT,
        CANCEL,
        state=EntrySG.comment,
        getter=get_texts_entry_dialog,
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
        SwitchTo(
            Format("{texts_dialog[change_systolic]}"),
            state=EntrySG.systolic,
            id="to_systolic",
        ),
        SwitchTo(
            Format("{texts_dialog[change_diastolic]}"),
            state=EntrySG.diastolic,
            id="to_diastolic",
        ),
        SwitchTo(
            Format("{texts_dialog[change_pulse]}"),
            state=EntrySG.pulse,
            id="to_pulse",
        ),
        SwitchTo(
            Format("{texts_dialog[change_arrhythmia]}"),
            state=EntrySG.arrhythmia,
            id="to_arrhythmia",
        ),
        SwitchTo(
            Format("{texts_dialog[change_comment]}"),
            state=EntrySG.comment,
            id="to_comment",
        ),
        SwitchTo(
            Format("{texts_dialog[save_data]}"),
            state=EntrySG.save_data,
            id="save_data",
        ),
        CANCEL,
        state=EntrySG.preview,
        getter=result_getter,
        parse_mode="html",
    ),
    Window(
        Format(text="{press_save}"),
        SwitchTo(
            text=Format("{save_data}"),
            id="save_data_button",
            on_click=save_data,
            state=EntrySG.finished,
        ),
        CANCEL,
        state=EntrySG.save_data,
        getter=get_texts_entry_dialog,
    ),
    WindowFinished(state=EntrySG.finished, txt="{save_result}"),
)
