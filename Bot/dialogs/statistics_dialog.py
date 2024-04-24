import logging

from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Cancel, Button, SwitchTo
from aiogram_dialog.widgets.text import Format

from databases.database import session_maker
from databases.orm_query import orm_get_user_data
from dialogs.getters.getters import get_number_rows_userdata
from states.states import StatisticsSG
from utils.statistics_graph import data_num_lines, create_statistics

logger = logging.getLogger(__name__)


async def get_statistic(
    callback: CallbackQuery, button: Button, dialog_manager: DialogManager
) -> None:
    data = await orm_get_user_data(
        session_maker, int(dialog_manager.event.from_user.id)
    )
    values = data_num_lines(data, 45)
    create_statistics(values, int(dialog_manager.event.from_user.id))
    graph = FSInputFile(f"./tables/{int(dialog_manager.event.from_user.id)}.png")

    await callback.message.answer_photo(graph)


statistics_dialog = Dialog(
    Window(
        Format(
            text="{show_or_cancel_graph}",
            when="rows_3_yes",
        ),
        Format(
            "{three_diary_entries}",
            when="rows_3_no",
        ),
        Cancel(Format("{start}"), when="rows_3_no"),
        SwitchTo(
            Format("{show_graph}"),
            id="graph",
            on_click=get_statistic,
            when="rows_3_yes",
            state=StatisticsSG.finished,
        ),
        Cancel(
            Format("{but_cancel}"),
            when="rows_3_yes",
        ),
        state=StatisticsSG.first,
        getter=get_number_rows_userdata,
    ),
    Window(
        Format("{press_start}"),
        Cancel(Format("{start}")),
        state=StatisticsSG.finished,
        getter=get_number_rows_userdata,
    ),
)
