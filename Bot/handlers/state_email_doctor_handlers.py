"""
Хендлеры для ввода email врача
и отправки дневника на этот email
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from pyisemail import is_email

from database.postgresession import session_number_rows, session_get_all_notes
from handlers.state_entry_handlers import engine
from states.states import FSMEntryEmailDoctor
from utils.utils import send_email

router = Router()


##################### Запуск FSM по команде /doctor ######################################################

@router.message(Command(commands='doctor'), StateFilter(default_state))
async def email_command(message: Message, state: FSMContext):
    """
    Этот хендлер будет срабатывать на команду /doctor в состоянии
    по умолчанию.
    Проверяем есть ли пользователь в БД.
    Если user есть в БД переводит бота в состояние ожидания ввода email
    Если такого user нет прекращаем работу машины
    """
    user_id = message.from_user.id

    if session_number_rows(engine, user_id) > 0:
        await message.answer(text='Введите email, на который будет выслан ваш дневник')
        # Устанавливаем состояние ожидания ввода email
        await state.set_state(FSMEntryEmailDoctor.doctor_email)
    else:
        await message.answer(text='У вас нет еще ни одной записи в дневнике, отправлять нечего.\n'
                                  'Сделайте хотя бы одну запись, а потом введите email')
        # Завершаем работу машины
        await state.clear()


@router.message(StateFilter(FSMEntryEmailDoctor.doctor_email))
async def email_entry(message: Message, state: FSMContext):
    """
    Извлекаем введенный email.
    Проверяем введенный email на валидность.
    Если email валидный, формируем дневник и отправляем его
    на предоставленный адрес, при этом отправляя сообщение,
    что дневник отправлен во вложении письмом по такому-то адресу.
    Если email не прошел валидацию сообщаем об ошибке.
    """
    email = message.text
    user_id = message.from_user.id

    bool_email = is_email(address=email, check_dns=True)

    if bool_email:
        session_get_all_notes(engine, user_id)
        send_email(email)
        await message.answer(text=f'Ваш дневник отправлен на электронный адрес:\n'
                                  f'{email}')
    else:
        await message.answer(text='Вы ошиблись, попробуйте снова ввести email.')

    # Завершаем работу машины
    await state.clear()
