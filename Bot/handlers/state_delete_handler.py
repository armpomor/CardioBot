"""
Хендлеры FSM для удаления дневника пользователя
"""

from aiogram import Router
from aiogram.filters import Command, StateFilter, Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from database.postgresession import session_delete_person
from handlers.state_entry_handlers import engine
from keyboards.inlane_keyboards import create_inline_kb
from states.states import FSMConfirmation

router = Router()


##################### Запуск FSM по команде /delete ######################################################

@router.message(Command(commands='delete'), StateFilter(default_state))
async def delete_command(message: Message, state: FSMContext):
    """
    Этот хендлер будет срабатывать на команду /delete в состоянии
    по умолчанию и переводить бота в состояние ожидания подтверждения
    """
    # Создаем инлайн-клаву для выбора месяца
    keyboard = create_inline_kb(width=1, Да='yes', Нет='no')
    await message.answer(text='Вы действительно хотите удалить все ваши записи?', reply_markup=keyboard)
    # Устанавливаем состояние ожидания нажатия кнопки
    await state.set_state(FSMConfirmation.confirmation)


@router.message(StateFilter(FSMConfirmation.confirmation))
async def warning_not_delete(message: Message):
    """
    Срабатывает если при подтверждении удаления дневника введено что-то некорректное
    """
    await message.answer(text='Пожалуйста, пользуйтесь предложенными кнопками.')


@router.callback_query(StateFilter(FSMConfirmation.confirmation), Text(text=['yes']))
async def delete_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает при подтверждении удалить записи и удаляем дневник по user_id
    """
    # Удаляем сообщение с кнопками, чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()
    # Удаляем все записи по user_id
    session_delete_person(engine, callback.message.chat.id)

    await callback.message.answer(text='Все ваши записи удалены из базы данных.')
    # Завершаем работу машины
    await state.clear()


@router.callback_query(StateFilter(FSMConfirmation.confirmation), Text(text=['no']))
async def delete_not_press(callback: CallbackQuery, state: FSMContext):
    """
    Хендлер срабатывает при отказе удалить записи
    """
    # Удаляем сообщение с кнопками, чтобы у пользователя не было желания тыкать кнопки
    await callback.message.delete()

    await callback.message.answer(text='Удаление дневника отменено.')
    # Завершаем работу машины
    await state.clear()
