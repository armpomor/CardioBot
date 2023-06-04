"""
Хендлеры машины состояния
при введении значений в таблицу БД
только что измеренных и за пошедшую дату
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database.postgresession import connect_db, session_add, session_get_email_notes, session_number_rows, \
    session_get_timezone_notes
from keyboards.inlane_keyboards import create_inline_kb, kb_inline_days
from states.states import FSMFillTable
from utils.utils import add_datetime

router = Router()

# Соединяемся с БД, создаем таблицу и движок engine
engine = connect_db()


@router.message(Command(commands='stop'), ~StateFilter(default_state))
async def stop_command_state(message: Message, state: FSMContext):
    """
    Этот хэндлер будет срабатывать на команду "/stop" в любых состояниях,
    кроме состояния по умолчанию, и отключать машину состояний,
    т.е. отменять ввод данных
    """
    await message.answer(text='Вы прервали ввод данных\n'
                              'Чтобы снова ввести данные в дневник '
                              'отправьте соответствующую команду')
    # Сбрасываем состояние
    await state.clear()


##################### Запуск FSM по команде /missed ######################################################

@router.message(Command(commands='missed'), StateFilter(default_state))
async def missed_command(message: Message, state: FSMContext):
    """
    Этот хендлер будет срабатывать на команду /missed в состоянии
    по умолчанию и переводить бота в состояние ожидания выбора месяца
    """
    # Создаем инлайн-клаву для выбора месяца
    keyboard = create_inline_kb(width=4, январь=1, февраль=2, март=3,
                                апрель=4, май=5, июнь=6, июль=7,
                                август=8, сентябрь=9, октябрь=10,
                                ноябрь=11, декабрь=12)
    await message.answer(text=f'Выберете месяц когда были сделаны измерения', reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода месяца
    await state.set_state(FSMFillTable.fill_month)


@router.callback_query(StateFilter(FSMFillTable.fill_month), Text(text=[str(x) for x in range(1, 13)]))
async def month_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает на нажатие кнопки при выборе месяца и переводит
    в состояние выбора дня. Сохраняем ответ (callback.data нажатой кнопки)
    в хранилище по ключу month
    """
    await state.update_data(month=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - выбор числа месяца
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    # Создаем инлайн-клаву для выбора числа
    keyboard = kb_inline_days()
    await callback.message.answer(text='Теперь выберете число месяца, когда сделать запись', reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора числа
    await state.set_state(FSMFillTable.fill_day)


@router.message(StateFilter(FSMFillTable.fill_month))
async def warning_not_month(message: Message):
    """
    Если при выборе месяца будет отправлено что-то некорректное
    """
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе месяца\n\nЕсли вы хотите прервать '
                              'ввод данных - отправьте команду /stop')


@router.callback_query(StateFilter(FSMFillTable.fill_day), Text(text=[str(x) for x in range(1, 32)]))
async def day_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает на нажатие кнопки при выборе числа месяца и переводит
    в состояние выбора времени. Сохраняем ответ (callback.data нажатой кнопки)
    в хранилище по ключу day
    """
    await state.update_data(day=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - выбор времени
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    # Создаем инлайн-клаву для выбора утро-полдень-вечер
    keyboard = create_inline_kb(width=1, утро='morning', полдень='noon', вечер='evening')
    await callback.message.answer(text='Теперь выберете время записи', reply_markup=keyboard)
    # Устанавливаем состояние ожидания выбора времени
    await state.set_state(FSMFillTable.fill_time)


@router.message(StateFilter(FSMFillTable.fill_day))
async def warning_not_day(message: Message):
    """
    Если при выборе числа месяца будет отправлено что-то некорректное
    """
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе дня\n\nЕсли вы хотите прервать '
                              'ввод данных - отправьте команду /stop')


@router.callback_query(StateFilter(FSMFillTable.fill_time), Text(text=['morning', 'noon', 'evening']))
async def month_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает на нажатие кнопки при выборе времени и переводит
    в состояние ожидания ввода верхнего давления. Сохраняем ответ (callback.data нажатой кнопки)
    в хранилище по ключу time
    """
    await state.update_data(time=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - выбор числа месяца
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text='Введите показатель верхнего (систолического) давления')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMFillTable.fill_systolic)


@router.message(StateFilter(FSMFillTable.fill_day))
async def warning_not_day(message: Message):
    """
    Если при выборе времени будет отправлено что-то некорректное
    """
    await message.answer(text='Пожалуйста, при выборе пользуйтесь кнопками\n\n '
                              'Если вы хотите прервать '
                              'ввод данных - отправьте команду /stop')


########################### Запуск FSM по команде /entry ##########################################################


@router.message(Command(commands='entry'), StateFilter(default_state))
async def entry_command(message: Message, state: FSMContext):
    """ 
    Этот хендлер будет срабатывать на команды /entry в состоянии
    по умолчанию и переводить бота в состояние ожидания ввода верхнего давления
    """
    await message.answer(text='Введите показатель верхнего (систолического) давления')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMFillTable.fill_systolic)


@router.message(StateFilter(FSMFillTable.fill_systolic), lambda x: x.text.isdigit() and 80 <= int(x.text) <= 270)
async def systolic_sent(message: Message, state: FSMContext):
    """
    Этот хэндлер будет срабатывать, если введено корректное
    значение верхнего давления и переводить в состояние
    ожидания ввода нижнего давления
    """
    # Сохраняем введенное значение в хранилище по ключу systolic
    await state.update_data(systolic=int(message.text))
    await message.answer(text='Теперь введите показатель нижнего (диастолического) давления')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMFillTable.fill_diastolic)


@router.message(StateFilter(FSMFillTable.fill_systolic))
async def warning_not_systolic(message: Message):
    """
    Если введено некорректное значение верхнего давления
    """
    await message.answer(text='Похоже вы отправили некорректное значение верхнего давления.\n'
                              'Пожалуйста, введите его заново\n\n'
                              'Если вы хотите прервать заполнение дневника - '
                              'отправьте команду /stop')


@router.message(StateFilter(FSMFillTable.fill_diastolic), lambda x: x.text.isdigit() and 40 <= int(x.text) <= 200)
async def diastolic_sent(message: Message, state: FSMContext):
    """
    Этот хэндлер будет срабатывать, если введено корректное
    значение нижнего давления и переводить в состояние
    ожидания ввода пульса
    """
    # Сохраняем введенное значение в хранилище по ключу diastolic
    await state.update_data(diastolic=int(message.text))
    await message.answer(text='Теперь введите показатель вашего пульса.\n'
                              'Если вы пульс не измеряли введи ноль.')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMFillTable.fill_pulse)


@router.message(StateFilter(FSMFillTable.fill_diastolic))
async def warning_not_diastolic(message: Message):
    """
    Если введено некорректное значение нижнего давления
    """
    await message.answer(text='Похоже вы отправили некорректное значение нижнего давления.\n'
                              'Пожалуйста, введите его заново\n\n'
                              'Если вы хотите прервать заполнение дневника - '
                              'отправьте команду /stop')


@router.message(StateFilter(FSMFillTable.fill_pulse), lambda x: x.text.isdigit() and 0 <= int(x.text) <= 200)
async def pulse_sent(message: Message, state: FSMContext):
    """
    Этот хэндлер будет срабатывать, если введено корректное
    значение пульса и переводить в состояние
    ожидания ввода наличия аритмии
    """
    # Сохраняем введенное значение в хранилище по ключу pulse
    await state.update_data(pulse=int(message.text))

    # Создаем инлайн-клаву
    keyboard = create_inline_kb(width=1, ДА='Да', НЕТ='Нет', НЕИЗВЕСТНО='Неизвестно')
    # Отправляем user сообщение с клавиатурой
    await message.answer(text='Теперь нажимая на кнопку,\n '
                              'отметьте есть ли у вас, в данный момент аритмия',
                         reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMFillTable.fill_arythmy)


@router.message(StateFilter(FSMFillTable.fill_pulse))
async def warning_not_pulse(message: Message):
    """
    Если введено некорректное значение пульса
    """
    await message.answer(text='Похоже вы отправили некорректное значение пульса.\n'
                              'Пожалуйста, введите его заново\n\n'
                              'Если вы хотите прервать заполнение дневника - '
                              'отправьте команду /stop')


@router.callback_query(StateFilter(FSMFillTable.fill_arythmy), Text(text=['Да', 'Нет', 'Неизвестно']))
async def arythmy_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает на нажатие кнопки при вопросе о наличии
    аритмии и переводит в состояние отправки комментария.
    Сохраняем ответ (callback.data нажатой кнопки)
    в хранилище по ключу arythmy
    """
    await state.update_data(arythmy=callback.data)
    # Удаляем сообщение с кнопками, потому что следующий этап - загрузка коммента
    # чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    await callback.message.answer(text='Теперь напишите в сообщении комментарий\n'
                                       'о вашем самочувствии и какие были приняты лекарства')
    # Устанавливаем состояние ожидания загрузки коммента
    await state.set_state(FSMFillTable.fill_comment)


@router.message(StateFilter(FSMFillTable.fill_arythmy))
async def warning_not_arythmy(message: Message):
    """
    Если при выборе наличия аритмии будет отправлено что-то некорректное
    """
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе наличия аритмии\n\nЕсли вы хотите прервать '
                              'ввод данных - отправьте команду /stop')


@router.message(StateFilter(FSMFillTable.fill_comment))
async def comment_sent(message: Message, state: FSMContext):
    """
    Срабатывает если получен коммент.
    Данные сохраняются и работа машины завершается
    """
    # Сохраняем введенный коммент по ключу comment, ник пользователя по ключу name
    # user_id по id
    await state.update_data(comment=message.text)
    await state.update_data(name=message.from_user.first_name)
    await state.update_data(user_id=message.from_user.id)

    # Сохраняем переданные данные в переменной user
    user = await state.get_data()

    # Проверяем есть ли у user записи и часовой пояс в них, если есть и добавляем его
    if session_number_rows(engine, message.from_user.id) > 0:
        user['timezone'] = session_get_timezone_notes(engine, message.from_user.id)
        # Если timezone is None тогда делаем часовой пояс московский
        if user['timezone'] is None:
            user['timezone'] = 0
    else:
        user['timezone'] = 0

    # Добавляем в user date_time
    user = add_datetime(user, user['timezone'])

    # Проверяем есть ли у user записи и email в них и добавляем его
    if session_number_rows(engine, message.from_user.id) > 0:
        user['email'] = session_get_email_notes(engine, message.from_user.id)

    # Добавляем полученные данные в БД
    session_add(user, engine)

    await state.clear()
    # Отправляем сообщение, что данные сохранены
    await message.answer(text='Ваши данные сохранены!')
