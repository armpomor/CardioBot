from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format

from dialogs.getters.getters import get_username
from states.states import (
    StartSG,
    EntrySG,
    TimezoneSG,
    TableOutputSG,
    DeleteSG,
    DoctorSG,
    StatisticsSG,
    SendSG,
    EmailSG,
    TableWidgetsSG,
)

start_dialog = Dialog(
    Window(
        Format(text="{hello}"),
        Format(text="{first_text}"),
        Start(
            Format(text="{entry}".ljust(150)),
            id="entry",
            state=EntrySG.systolic,
        ),
        Start(
            Format(text="{missed}".ljust(150)),
            id="missed",
            state=EntrySG.date,
        ),
        Start(
            Format(text="{timezone}".ljust(150)),
            id="timezone",
            state=TimezoneSG.first,
        ),
        Start(
            Format(text="{entries_display}".ljust(150)),
            id="table_widgets",
            state=TableWidgetsSG.zero,
        ),
        Start(
            Format(text="{get_diary}".ljust(150)),
            id="table_output",
            state=TableOutputSG.zero,
        ),
        Start(
            Format(text="{statistics}".ljust(150)),
            id="statistics",
            state=StatisticsSG.first,
        ),
        Start(
            Format(text="{delete_diary}".ljust(150)),
            id="delete",
            state=DeleteSG.zero,
        ),
        Start(
            Format(text="{input_email}".ljust(150)),
            id="email",
            state=EmailSG.first,
        ),
        Start(
            Format(text="{send_diary}".ljust(150)),
            id="send",
            state=SendSG.zero,
        ),
        Start(
            Format(text="{send_doctor}".ljust(150)),
            id="doctor",
            state=DoctorSG.zero,
        ),
        getter=get_username,
        state=StartSG.start,
    ),
)
