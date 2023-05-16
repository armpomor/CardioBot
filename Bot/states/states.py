from aiogram.filters.state import State, StatesGroup


class FSMFillTable(StatesGroup):
    """
    Машина состояния ввода данных
    """
    fill_month = State()  # Состояние ожидания ввода месяца
    fill_day = State()  # Состояние ожидания ввода дня
    fill_time = State()  # Состояние ожидания ввода времени
    fill_systolic = State()  # Состояние ожидания ввода верхнего давления 80-240
    fill_diastolic = State()  # Состояние ожидания ввода нижнего давления 50-160
    fill_pulse = State()  # Состояние ожидания ввода пульса 40-160
    fill_arythmy = State()  # Состояние ожидания ввода аритмия
    fill_comment = State()  # Состояние ожидания ввода комментария о состоянии и препаратах


class FSMChangeNote(StatesGroup):
    """
    Машина состояния изменения записи в таблице
    """
    fill_systolic = State()  # Состояние ожидания ввода верхнего давления 80-240
    fill_diastolic = State()  # Состояние ожидания ввода нижнего давления 50-160
    fill_pulse = State()  # Состояние ожидания ввода пульса 40-160
    fill_arythmy = State()  # Состояние ожидания ввода аритмия
    fill_comment = State()  # Состояние ожидания ввода комментария о состоянии и препаратах


class FSMConfirmation(StatesGroup):
    """
    FSM удаления всех записей определенного user,
    а также для изменения последней записи.
    Работает с кнопкой Да Нет
    """
    confirmation = State()  # Состояние ожидания ввода подтверждения


class FSMEntryEmail(StatesGroup):
    """
    FSM ввода email
    """
    fill_email = State()  # Состояние ожидания ввода email


class FSMEntryEmailDoctor(StatesGroup):
    """
    FSM ввода email врача
    и отправки ему дневника
    """
    doctor_email = State()  # Состояние ожидания ввода email


class FSMEntryTimezone(StatesGroup):
    """
    FSM ввода часового пояса
    """
    fill_timezone = State()  # Состояние ожидания ввода timezone
