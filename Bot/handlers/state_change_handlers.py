"""
Хендлеры машины состояния при изменении последней записи пользователя
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database.postgresession import session_add, session_last_date, session_number_rows, session_delete_note, \
    session_get_email_notes
from handlers.state_entry_handlers import engine
from keyboards.inlane_keyboards import create_inline_kb
from states.states import FSMConfirmation, FSMChangeNote

router = Router()


##################### Запуск FSM по команде /change ######################################################

@router.message(Command(commands='change'), StateFilter(default_state))
async def change_command(message: Message, state: FSMContext):
    """
    Этот хендлер будет срабатывать на команды /change в состоянии
    по умолчанию, проверять есть ли у user записи в БД.
    Если такого user нет останавливать машину.
    Если есть переводим в режим ожидания подтверждения изменения.
    """
    # Создаем инлайн-клаву для выбора ответа
    keyboard = create_inline_kb(width=1, Да='да', Отмена='нет')
    user_id = message.from_user.id
    if session_number_rows(engine, user_id) > 0:
        await message.answer(text=f'Последняя запись была вами сделана {session_last_date(engine, user_id).date_time}\n'
                                  'Изменим ее?\n', reply_markup=keyboard)
        # Устанавливаем состояние ожидания подтверждения или отмены изменения
        await state.set_state(FSMConfirmation.confirmation)
    else:
        await message.answer(text='У вас нет ни одной записи в дневнике.\n'
                                  'Изменять нечего.')
        # Завершаем работу машины
        await state.clear()


@router.message(StateFilter(FSMConfirmation.confirmation))
async def warning_not_change(message: Message):
    """
    Срабатывает если при подтверждении изменения записи введено что-то некорректное
    """
    await message.answer(text='Пожалуйста, пользуйтесь предложенными кнопками.')


@router.callback_query(StateFilter(FSMConfirmation.confirmation), Text(text=['нет']))
async def change_not_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает при отказе изменить запись
    """
    # Удаляем сообщение с кнопками, чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()

    await callback.message.answer(text='Изменение последней записи отменено.')
    # Завершаем работу машины
    await state.clear()


########################### Запуск FSMChangeNote ##########################################################
@router.callback_query(StateFilter(FSMConfirmation.confirmation), Text(text=['да']))
async def change_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает при подтверждении изменить последнюю запись.
    Запускается FSMFillTable
    """
    # Удаляем сообщение с кнопками, чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()

    user_id = callback.message.chat.id

    await callback.message.answer(text='Введите показатель верхнего (систолического) давления\n'
                                       f'Прошлая запись:\n {session_last_date(engine, user_id).systolic}')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMChangeNote.fill_systolic)


@router.message(StateFilter(FSMChangeNote.fill_systolic), lambda x: x.text.isdigit() and 80 <= int(x.text) <= 270)
async def systolic_sent(message: Message, state: FSMContext):
    """
    Этот хэндлер будет срабатывать, если введено корректное
    значение верхнего давления и переводить в состояние
    ожидания ввода нижнего давления
    """
    # Сохраняем введенное значение в хранилище по ключу systolic
    await state.update_data(systolic=int(message.text))

    user_id = message.from_user.id
    await message.answer(text='Теперь введите показатель нижнего (диастолического) давления\n'
                              f'Прошлая запись:\n {session_last_date(engine, user_id).diastolic}')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMChangeNote.fill_diastolic)


@router.message(StateFilter(FSMChangeNote.fill_systolic))
async def warning_not_systolic(message: Message):
    """
    Если введено некорректное значение верхнего давления
    """
    await message.answer(text='Похоже вы отправили некорректное значение верхнего давления.\n'
                              'Пожалуйста, введите его заново\n\n'
                              'Если вы хотите прервать заполнение дневника - '
                              'отправьте команду /stop')


@router.message(StateFilter(FSMChangeNote.fill_diastolic), lambda x: x.text.isdigit() and 40 <= int(x.text) <= 200)
async def diastolic_sent(message: Message, state: FSMContext):
    """
    Этот хэндлер будет срабатывать, если введено корректное
    значение нижнего давления и переводить в состояние
    ожидания ввода пульса
    """
    # Сохраняем введенное значение в хранилище по ключу diastolic
    await state.update_data(diastolic=int(message.text))

    user_id = message.from_user.id
    await message.answer(text='Теперь введите показатель вашего пульса.\n'
                              'Если вы пульс не измеряли введи ноль.\n'
                              f'Прошлая запись:\n {session_last_date(engine, user_id).pulse}')
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMChangeNote.fill_pulse)


@router.message(StateFilter(FSMChangeNote.fill_diastolic))
async def warning_not_diastolic(message: Message):
    """
    Если введено некорректное значение нижнего давления
    """
    await message.answer(text='Похоже вы отправили некорректное значение нижнего давления.\n'
                              'Пожалуйста, введите его заново\n\n'
                              'Если вы хотите прервать заполнение дневника - '
                              'отправьте команду /stop')


@router.message(StateFilter(FSMChangeNote.fill_pulse), lambda x: x.text.isdigit() and 0 <= int(x.text) <= 200)
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

    user_id = message.from_user.id
    # Отправляем user сообщение с клавиатурой
    await message.answer(text='Теперь нажимая на кнопку,\n '
                              'отметьте есть ли у вас, в данный момент аритмия\n'
                              f'Прошлая запись:\n {session_last_date(engine, user_id).arythmy}',
                         reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода
    await state.set_state(FSMChangeNote.fill_arythmy)


@router.message(StateFilter(FSMChangeNote.fill_pulse))
async def warning_not_pulse(message: Message):
    """
    Если введено некорректное значение пульса
    """
    await message.answer(text='Похоже вы отправили некорректное значение пульса.\n'
                              'Пожалуйста, введите его заново\n\n'
                              'Если вы хотите прервать заполнение дневника - '
                              'отправьте команду /stop')


@router.callback_query(StateFilter(FSMChangeNote.fill_arythmy), Text(text=['Да', 'Нет', 'Неизвестно']))
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

    user_id = callback.message.chat.id
    await callback.message.answer(text='Теперь напишите в сообщении комментарий\n'
                                       'о вашем самочувствии и какие были приняты лекарства.\n'
                                       f'Прошлый ваш комментарий:\n {session_last_date(engine, user_id).comment}')
    # Устанавливаем состояние ожидания загрузки коммента
    await state.set_state(FSMChangeNote.fill_comment)


@router.message(StateFilter(FSMChangeNote.fill_arythmy))
async def warning_not_arythmy(message: Message):
    """
    Если при выборе наличия аритмии будет отправлено что-то некорректное
    """
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе наличия аритмии\n\nЕсли вы хотите прервать '
                              'ввод данных - отправьте команду /stop')


@router.message(StateFilter(FSMChangeNote.fill_comment))
async def comment_sent(message: Message, state: FSMContext):
    """
    Срабатывает если получен коммент.
    Данные сохраняются и работа машины завершается
    """
    # Сохраняем введенный коммент по ключу comment, ник пользователя по ключу name
    # user_id по id

    user_id = message.from_user.id

    await state.update_data(comment=message.text)
    await state.update_data(name=message.from_user.first_name)
    await state.update_data(user_id=user_id)

    # Сохраняем переданные данные в переменной user
    user = await state.get_data()

    # Извлекаем параметры id записи и date_time из последней записи user
    id_note = session_last_date(engine, user_id).id
    date_time = session_last_date(engine, user_id).date_time

    # Удаляем последнюю запись по id_note, которая является id записи
    session_delete_note(engine, id_note)

    # Добавляем в user date_time
    user['date_time'] = date_time

    # Проверяем есть ли у user email и добавляем его
    user['email'] = session_get_email_notes(engine, message.from_user.id)

    # Добавляем полученные данные в БД
    session_add(user, engine)

    # Завершаем работу машины
    await state.clear()
    # Отправляем сообщение, что данные сохранены
    await message.answer(text='Ваша последняя запись изменена.')
