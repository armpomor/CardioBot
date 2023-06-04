"""
Хендлеры для ввода email
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from pyisemail import is_email

from database.postgresession import session_add_email, session_number_rows
from handlers.state_entry_handlers import engine
from states.states import FSMEntryEmail

router = Router()


##################### Запуск FSM по команде /email ######################################################

@router.message(Command(commands='email'), StateFilter(default_state))
async def email_command(message: Message, state: FSMContext):
    """
    Этот хендлер будет срабатывать на команду /email в состоянии
    по умолчанию.
    Проверяем есть ли пользователь в БД.
    Если user есть в БД переводит бота в состояние ожидания ввода email
    Если такого user нет прекращаем работу машины
    """
    user_id = message.from_user.id

    if session_number_rows(engine, user_id) > 0:
        await message.answer(text='Введите email, на который будет выслан ваш дневник')
        # Устанавливаем состояние ожидания ввода email
        await state.set_state(FSMEntryEmail.fill_email)
    else:
        await message.answer(text='У вас нет еще ни одной записи в дневнике, отправлять нечего.\n'
                                  'Сделайте хотя бы одну запись, а потом введите email')
        await state.clear()


@router.message(StateFilter(FSMEntryEmail.fill_email))
async def email_entry(message: Message, state: FSMContext):
    """
    Извлекаем введенный email.
    Проверяем введенный email на валидность.
    Если email валидный тогда сохраняем его.
    Если email не прошел валидацию сообщаем об ошибке.
    """
    email = message.text
    user_id = message.from_user.id

    bool_email = is_email(address=email, check_dns=True)

    if bool_email:
        session_add_email(engine, user_id, email)
        await message.answer(text='email добавлен и обновлен.')
    else:
        await message.answer(text='Вы ввели некорректный email.\n'
                                  'Попробуйте снова.')
    await state.clear()
