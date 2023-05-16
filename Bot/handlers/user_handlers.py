from aiogram import Router
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram.types import Message, FSInputFile

from database.postgresession import session_number_rows, session_last_date, session_get_email_notes, \
    session_get_all_notes
from handlers.state_entry_handlers import engine
from lexicon.lexicon import LEXICON
from utils.statistics import create_statistics
from utils.utils import send_email, preparation_data

router = Router()


@router.message(CommandStart(), StateFilter(default_state))
async def start_command(message: Message):
    """
    Команда /start отправляем сообщение с приветствием
    и описанием бота. Хендлер будет работать вне состояний
    """
    await message.answer(LEXICON['/start'], parse_mode='HTML', disable_web_page_preview=True)


@router.message(Command(commands='help'), StateFilter(default_state))
async def help_command(message: Message):
    """
    Команда "/help" отправляет пользователю сообщение
    со списком доступных команд в боте.
    Хендлер будет работать вне состояний
    """
    await message.answer(LEXICON['/help'], parse_mode='HTML')


@router.message(Command(commands='stop'), StateFilter(default_state))
async def stop_command(message: Message):
    """
    Этот хэндлер будет срабатывать на команду "/stop"
    в состоянии по умолчанию
    """
    await message.answer(text='Отменять нечего.\n\n'
                              'Чтобы ввести данные в дневник '
                              'отправьте команду /entry')


@router.message(Command(commands='send'), StateFilter(default_state))
async def send_email_command(message: Message):
    """
    Срабатывает на команду /send в состоянии по умолчанию.
    Сначала проверяет есть ли у пользователя записи в дневнике и сохраненный адрес
    Если все есть, формирует дневник и отправляет его на предоставленный адрес,
    при этом отправляя сообщение, что дневник отправлен во вложении письмом
    по такому-то адресу. Если нет, предлагает сначала ввести адрес командой /email
    или сделать записи в дневнике
    """
    user_id = message.from_user.id

    if session_number_rows(engine, user_id) > 0 and session_get_email_notes(engine, user_id) is not None:
        session_get_all_notes(engine, user_id)
        send_email(session_last_date(engine, user_id).email)
        await message.answer(text=f'Ваш дневник отправлен на электронный адрес:\n'
                                  f'{session_last_date(engine, user_id).email}')
    else:
        await message.answer(text='Введите сначала email командой /email, чтобы я смог отправить дневник.')


@router.message(Command(commands='statistics'), StateFilter(default_state))
async def statistic_command(message: Message):
    """
    Срабатывает на команду /week в состоянии по умолчанию.
    Сначала проверяет сколько у пользователя записей в дневнике.
    Если больше двух, тогда извлекаем 45 последних записей пользователя,
    строим график статистики и отправляем ее в виде графика в чат.
    Если две или меньше, отправляет сообщение о том, что для
    статистики мало записей.
    """
    user_id = message.from_user.id
    if session_number_rows(engine, user_id) > 2:
        data = session_get_all_notes(engine, user_id)
        values = preparation_data(data)
        create_statistics(values)
        photo = FSInputFile('diary/Diary.png')
        await message.answer_photo(photo)
    else:
        await message.answer(text='Для построения статистического графика у вас мало записей в дневнике.\n'
                                  'Необходимый минимум три записи.')


@router.message(StateFilter(default_state))
async def echo(message: Message):
    """
    Срабатывает если в чат пишут непредусмотренное командами
    """
    await message.reply(text="Я не понимаю такой команды.\n"
                             "Пользуйтесь кнопками или нажмите /help.")
