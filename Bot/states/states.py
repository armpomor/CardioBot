from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class EntrySG(StatesGroup):
    date = State()  # Date input waiting state
    time = State()  # Timing
    systolic = State()  # Upper pressure input waiting state 60-240
    diastolic = State()  # Low pressure input waiting state 300-180
    pulse = State()  # Pulse input waiting state 30-200
    arrhythmia = State()
    comment = State()
    preview = State()
    save_data = State()
    finished = State()


class TimezoneSG(StatesGroup):
    first = State()
    save = State()
    finished = State()


class TableOutputSG(StatesGroup):
    zero = State()
    first = State()


class SendSG(StatesGroup):
    zero = State()
    first = State()
    finished = State()


class DoctorSG(StatesGroup):
    zero = State()
    first = State()
    second = State()
    finished = State()


class EmailSG(StatesGroup):
    first = State()
    save = State()
    finished = State()


class StatisticsSG(StatesGroup):
    first = State()
    finished = State()


class DeleteSG(StatesGroup):
    zero = State()
    delete = State()
    finished = State()


class TableWidgetsSG(StatesGroup):
    zero = State()
    first = State()
    delete = State()
    systolic = State()
    diastolic = State()
    pulse = State()
    arrhythmia = State()
    comment = State()
    update_data = State()
    save_data = State()
