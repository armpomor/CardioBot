"""
Хендлеры FSM устанавливают часовой пояс пользователя
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database.postgresession import session_number_rows, session_add_timezone
from handlers.state_entry_handlers import engine
from keyboards.inlane_keyboards import create_inline_kb
from states.states import FSMEntryTimezone

router = Router()


##################### Запуск FSM по команде /timezone ######################################################

@router.message(Command(commands='timezone'), StateFilter(default_state))
async def timezone_command(message: Message, state: FSMContext):
    """
    Срабатывает на команду /timezone в состоянии
    по умолчанию и переводить бота в состояние
    ожидания нажатия кнопки с часовым поясом
    """
    # Создаем инлайн-клаву для выбора часового пояса
    keyboard = create_inline_kb(width=4, Калининград=-1,
                                Москва=0, Самара=1,
                                Екатеринбург=2, Омск=3,
                                Красноярск=4, Иркутск=5,
                                Якутск=6, Владивосток=7,
                                Магадан=8, Камчатка=9)
    await message.answer(text=f'Выберете часовой пояс, чтобы время в вашем дневнике отображалось корректно.',
                         reply_markup=keyboard)
    # Устанавливаем состояние ожидания ввода часового пояса
    await state.set_state(FSMEntryTimezone.fill_timezone)


@router.callback_query(StateFilter(FSMEntryTimezone.fill_timezone), Text(text=[str(x) for x in range(-1, 10)]))
async def timezone_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает при вводе часового пояса.
    Проверяет есть лм такой user в БД и если есть,
    заносит timezone в БД по user_id, а если нет сообщает,
    что необходима хотя бы одна запись в дневнике.
    """
    # Сохраняем переданный часовой пояс в переменной timezone
    timezone = callback.data
    # Удаляем сообщение с кнопками, чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()

    if session_number_rows(engine, callback.message.chat.id) > 0:
        session_add_timezone(engine, callback.message.chat.id, int(timezone))
    else:
        await callback.message.answer(
            text='Сделайте хотя бы одну запись в дневнике, а потом можно будет изменить часовой пояс.')

    await callback.message.answer(text='Часовой пояс изменен.')
    # Завершаем работу машины
    await state.clear()


@router.message(StateFilter(FSMEntryTimezone.fill_timezone))
async def warning_timezone(message: Message):
    """
    Срабатывает если введено что-то некорректное
    """
    await message.answer(text='Пожалуйста, пользуйтесь кнопками '
                              'при выборе часового пояса\n\nЕсли вы хотите прервать '
                              'ввод данных - отправьте команду /stop')
