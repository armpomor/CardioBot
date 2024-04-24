import logging
from datetime import datetime, timezone, timedelta
from typing import Any, TYPE_CHECKING

from aiogram.types import User
from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

from config.config_data import FINISHED
from databases.database import session_maker
from databases.orm_query import (
    orm_get_id_user,
    orm_get_user_timezone,
    orm_get_user_data,
    orm_get_user_email,
    orm_get_row_user_data,
)
from utils.data_checking import date_str

logger = logging.getLogger(__name__)


async def get_username(
    event_from_user: User, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    """
    Getter returning texts for start_dialog
    """
    username = event_from_user.first_name
    return {
        "hello": i18n.hello(username=username),
        "first_text": f"{i18n.firstrow()}\n"
        f"{i18n.secondrow()}\n"
        f"{i18n.thirdrow()}\n"
        f"{i18n.fourthrow()}"
        f" {i18n.fifthrow()}"
        f" {i18n.sixthrow()}\n"
        f"{i18n.seventhrow()}\n"
        f"{i18n.eighthrow()}\n"
        f"{i18n.ninthrow()}\n"
        f"{i18n.tenthrow()}"
        " <a href='cardiobot.100@gmail.com'>cardiobot.100@gmail.com</a>\n"
        f"{i18n.eleventhrow()}\n"
        f"{i18n.twelfthrow()} "
        f"<a href='https://docs.google.com/document/d/1K0ov9JfTZ8b2UxLseGRQu4ZKyLi29Hymsk6TGO-Dw_0/edit?usp=sharing'>{i18n.thirteenthrow()}</a>.\n"
        f"<b>{i18n.fourteenthrow()}</b>\n"
        f"&#128138; https://t.me/FarmacyDrugsBot {i18n.fiveteenthrow()}\n"
        f"&#128138; https://t.me/Medicines100bot {i18n.sixteenthrow()}\n"
        f"&#9752; https://t.me/Medicinal_Plants_Bot {i18n.seventeenthrow()}\n"
        f"{i18n.eighteenthrow()}",
        "entry": i18n.entry(),
        "missed": i18n.missed(),
        "timezone": i18n.timezone(),
        "entries_display": i18n.entries.display(),
        "get_diary": i18n.geting.diary(),
        "statistics": i18n.statistics(),
        "delete_diary": i18n.deletion.diary(),
        "input_email": i18n.enter.email(),
        "send_diary": i18n.diary.send(),
        "send_doctor": i18n.doctor.send(),
    }


async def get_user_id(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, int | str]:
    """
    Getter returning user_id and texts for dialogs
    """
    texts = {
        "quest_delete": i18n.quest.deletion(),
        "delete": i18n.deletion(),
        "no_delete": i18n.cancel.deletion(),
    }
    return {"user_id": int(dialog_manager.event.from_user.id)} | texts


async def result_getter(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, dict[str, Any] | str]:
    """
    A getter that returns a dictionary containing the key
    result_data the entered data is saved in the form of
    a dictionary, under the texts_dialog key the texts for
    the input_dialog and for the table_widgets_dialog, and
    under the entry_cancel key the text for the custom widget CANCEL
    """
    dialog_manager.dialog_data[FINISHED] = True

    tz = await orm_get_user_timezone(
        session_maker, int(dialog_manager.event.from_user.id)
    )

    if dialog_manager.dialog_data.get("date_time"):
        date_time = dialog_manager.dialog_data.get("date_time")
    else:
        date_time = datetime(
            datetime.now(timezone(timedelta(hours=tz))).year,
            datetime.now(timezone(timedelta(hours=tz))).month,
            datetime.now(timezone(timedelta(hours=tz))).day,
            datetime.now(timezone(timedelta(hours=tz))).hour,
            datetime.now().minute,
        )

    result_data = {
        "user_id": int(dialog_manager.event.from_user.id),
        "pulse": dialog_manager.find("pulse").get_value(),
        "systolic": dialog_manager.find("systolic").get_value(),
        "diastolic": dialog_manager.find("diastolic").get_value(),
        "arrhythmia": dialog_manager.find("arrhythmia").get_checked(),
        "comment": dialog_manager.find("comment").get_value(),
        "name": dialog_manager.event.from_user.first_name,
        "language_code": dialog_manager.event.from_user.language_code,
        "date_time": date_time,
    }
    texts_dialog = {
        "change_systolic": i18n.change.systolic(),
        "change_diastolic": i18n.change.diastolic(),
        "change_pulse": i18n.change.pulse(),
        "change_arrhythmia": i18n.change.arrhythmia(),
        "change_comment": i18n.change.comment(),
        "save_data": i18n.save.data(),
        "you_entered": i18n.you.entered(),
        "systolic_press": i18n.systolic.press(),
        "diastolic_press": i18n.diastolic.press(),
        "pulse": i18n.pulse(),
        "arrhythmia": i18n.arrhythmia(),
        "comment": i18n.comment(),
    }
    keys = ["result_data", "texts_dialog"]
    values = [result_data, texts_dialog]

    return (
        dict(zip(keys, values))
        | {"entry_cancel": i18n.entry.cancel()}
        | {"cancel_edit": i18n.edit.cancel()}
    )


async def get_email(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    """
    Getter returns email and texts for dialogs
    """
    email = dialog_manager.find("email").get_value()

    texts = {
        "but_cancel": i18n.but.cancel(),
        "send": i18n.sending(),
        "send_cancel_diary": f"{i18n.sending_diary(email=email)}\n{i18n.press.cancel()}",
        "save_cancel_email": f"{i18n.you.entered()}: {email}.\n{i18n.save.email()} {i18n.press.cancel()}",
        "save": i18n.press.save(),
    }
    return {"email": dialog_manager.find("email").get_value()} | texts


async def get_user_email(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, Any]:
    """
    Getter returning 'email_yes': True and 'email_no': False
    if the user has a saved email. If not, then vice versa.
    Also 'email': 'user@example.com' or 'email': ''
    Texts for dialogues.
    """
    data_email = {"email": "", "email_yes": True, "email_no": False}
    email = await orm_get_user_email(
        session_maker, int(dialog_manager.event.from_user.id)
    )
    if email:
        data_email["email"] = email
        dialog_manager.dialog_data.update({"email": email})
    else:
        data_email["email_yes"] = False
        data_email["email_no"] = True

    texts = {
        "question_send": i18n.question_send(email=email),
        "send": i18n.sending(),
        "change_email": i18n.change_email(),
        "but_cancel": i18n.but.cancel(),
        "no_email": f"{i18n.no_email()}\n{i18n.next_start()}",
        "start": i18n.start(),
    }

    return data_email | texts


async def get_user_database(dialog_manager: DialogManager, **kwargs) -> dict[str, bool]:
    """
    Getter returning 'yes_user': True and 'no_user': False
    if user is in the database, otherwise vice versa.
    """
    user_id = int(dialog_manager.event.from_user.id)

    if len(await orm_get_id_user(session_maker, user_id)):
        yes, no = True, False
    else:
        yes, no = False, True

    return {"yes_user": yes, "no_user": no}


async def get_number_rows_userdata(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, bool | str]:
    """
    Getter returning 'rows_3_yes': True and 'rows_3_no': False
    if the number of rows in the UserData table is more than 2,
    otherwise vice versa. And 'rows_yes': True, 'rows_no': False
    if there is at least one record. Texts for dialogues are also returning
    """
    user_id = int(dialog_manager.event.from_user.id)
    num_rows = {
        "rows_3_yes": True,
        "rows_3_no": False,
        "rows_yes": True,
        "rows_no": False,
    }

    if len(await orm_get_user_data(session_maker, user_id)) < 1:
        num_rows["rows_3_yes"] = False
        num_rows["rows_3_no"] = True
        num_rows["rows_yes"] = False
        num_rows["rows_no"] = True
    elif len(await orm_get_user_data(session_maker, user_id)) < 3:
        num_rows["rows_3_yes"] = False
        num_rows["rows_3_no"] = True

    texts = {
        "no_data": f"{i18n.no_data()}\n" f"{i18n.next_start()}",
        "start": i18n.start(),
        "but_cancel": i18n.but.cancel(),
        "but_next": i18n.but_next(),
        "next_cancel_del_data": f"{i18n.next_del_data()}\n{i18n.press.cancel()}",
        "next_cancel_send_email": f"{i18n.next_send_email()}\n{i18n.press.cancel()}",
        "show_or_cancel_graph": f"{i18n.show_or_cancel_graph()}\n{i18n.press.cancel()}",
        "three_diary_entries": f"{i18n.three_diary_entries()}\n{i18n.next_start()}",
        "show_graph": i18n.show_graph(),
        "press_start": i18n.next_start(),
        "next_cancel_table": f"{i18n.next_table()}\n{i18n.press.cancel()}",
        "receive_diary": f"{i18n.receive_diary()}\n{i18n.press.cancel()}",
        "no_entry": f"{i18n.no_data()}\n{i18n.next_start()}",
        "get_table": i18n.get_table(),
        "next_cancel_display_entry": f"{i18n.next_display_entry()}\n{i18n.press.cancel()}",
    }

    return num_rows | texts


async def get_timezone(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, list[tuple[str, int]] | str]:
    tz = [
        (i18n.utc1(), 1),
        (i18n.utc2(), 2),
        (i18n.utc3(), 3),
        (i18n.utc4(), 4),
        (i18n.utc5(), 5),
        (i18n.utc6(), 6),
        (i18n.utc7(), 7),
        (i18n.utc8(), 8),
        (i18n.utc9(), 9),
        (i18n.utc10(), 10),
        (i18n.utc11(), 11),
        (i18n.utc12(), 12),
    ]
    texts = {
        "select_timezone": i18n.select_timezone(),
        "cancel_input": i18n.entry.cancel(),
        "save": i18n.press.save(),
        "but_cancel": i18n.but.cancel(),
        "save_cancel_timezone": f"{i18n.save_timezone()}\n{i18n.press.cancel()}",
    }

    return {"tz": tz} | texts


async def get_texts_finished(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    """
    The getter returns the texts for the final Window
    """
    return {
        "confirm_delete": f"{i18n.confirm_delete()}\n{i18n.next_start()}",
        "start": i18n.start(),
        "send_diary": f"{i18n.send_diary()}\n{i18n.next_start()}",
        "save_email": f"{i18n.save_email()}\n{i18n.next_start()}",
        "save_result": f"{i18n.save_result()}\n{i18n.next_start()}",
        "update_save": f"{i18n.update_save()}\n{i18n.next_start()}",
        "save_timezone": f"{i18n.saving_timezone()}\n{i18n.next_start()}",
    }


async def get_texts_input_email(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    """
    Getter returns Window texts for email input
    """
    return {
        "input_email": f"{i18n.input_email()}\n{i18n.press.cancel()}",
        "but_cancel": i18n.but.cancel(),
    }


async def get_texts_entry_dialog(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    """
    Getter returns texts for entry_dialog
    """
    return {
        "edit_cancel": i18n.edit_cancel(),
        "entry_cancel": i18n.entry.cancel(),
        "date_selection": i18n.date_selection(),
        "time_selection": i18n.time_selection(),
        "entry_systolic": i18n.entry_systolic(),
        "entry_diastolic": i18n.entry_diastolic(),
        "entry_pulse": f"{i18n.entry_pulse()}\n{i18n.entry_zero()}",
        "presence_arrhythmia": i18n.presence_arrhythmia(),
        "write_comment": i18n.write_comment(),
        "press_save": i18n.press_save(),
        "save_data": i18n.press.save(),
        "question_arrhythmia": [i18n.word_yes(), i18n.word_no(), i18n.unknown()],
    }


async def get_data(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, list[list[Any]] | str]:
    """
    Getter returning the last 20 records
    by key 'rows', in which datetime is converted to str
    The datetime of the string is stored in the variable and key 'result'.
    We also save the texts for table_widgets_dialog in the getter
    """
    user_id = int(dialog_manager.event.from_user.id)

    data = await orm_get_user_data(session_maker, user_id)
    data = date_str(data[-20:])

    # В dialog_data записываем datetime по ключу date_time
    date_time = dialog_manager.find("row").get_checked()
    if len(date_time):
        dialog_manager.dialog_data.update(
            {"date_time": datetime.strptime(date_time[0], "%Y-%m-%d %H:%M")}
        )
    result = dialog_manager.find("row").get_checked()

    if result:
        result = result[0]
        texts = {
            "delete_edit_row": i18n.delete_edit_row(result=result),
            "delete_row": i18n.delete_row(result=result),
            "edit_row": i18n.edit_row(result=result),
        }
    else:
        texts = dict()

    return {
        "rows": data,
        "result": dialog_manager.find("row").get_checked(),
        "mark_row": f"{i18n.mark_row()}\n",
        "but_cancel": i18n.but.cancel(),
    } | texts


async def get_row(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, list[Any] | str]:
    """
    Getter returning texts for table_widgets_dialog
    """
    user_id = int(dialog_manager.event.from_user.id)
    date_time = dialog_manager.find("row").get_checked()

    row = await orm_get_row_user_data(
        session_maker, user_id, datetime.strptime(date_time[0], "%Y-%m-%d %H:%M")
    )

    return {
        "cancel_edit": i18n.edit.cancel(),
        "edit_systolic": f"{i18n.entry_systolic()}\n{i18n.word_was()} {row.systolic}",
        "edit_diastolic": f"{i18n.entry_diastolic()}\n{i18n.word_was()} {row.diastolic}",
        "edit_pulse": f"{i18n.entry_pulse()}\n{i18n.word_was()} {row.pulse}",
        "edit_arrhythmia": f"{i18n.presence_arrhythmia()}\n{i18n.word_was()} {row.arrhythmia}",
        "edit_comment": f"{i18n.write_comment()}\n{i18n.word_was()} {row.comment}",
        "question_arrhythmia": [i18n.word_yes(), i18n.word_no(), i18n.unknown()],
    }


async def get_texts_dialogs(
    dialog_manager: DialogManager, i18n: TranslatorRunner, **kwargs
) -> dict[str, str]:
    """
    Getter returning texts for dialogs
    """
    return {
        "row_delete": f"{i18n.row_delete()}\n{i18n.next_start()}",
        "start": i18n.start(),
    }
