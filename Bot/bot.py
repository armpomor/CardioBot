import asyncio
import logging

from aiogram import Bot, Dispatcher

from config.config import TOKEN
# from config.config_dev import TOKEN
from handlers import user_handlers, state_entry_handlers, state_delete_handler, state_email_handlers, \
    state_change_handlers, state_email_doctor_handlers, state_timezone_handlers
from keyboards.set_menu import set_menu

# Инициализация логгера
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурирование логирование
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
               u'[%(asctime)s] - %(name)s - %(message)s')

    # Выводим  вконсоль информацию о начале запуска бота
    logger.info('Starting bot')

    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(state_entry_handlers.router)
    dp.include_router(state_timezone_handlers.router)
    dp.include_router(state_delete_handler.router)
    dp.include_router(state_email_handlers.router)
    dp.include_router(state_change_handlers.router)
    dp.include_router(state_email_doctor_handlers.router)
    dp.include_router(user_handlers.router)

    # Кнопка меню
    await set_menu(bot)

    # Запускаем polling
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        if __name__ == '__main__':
            asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        # Выводим в консоль сообщение об ошибке,
        # если получены исключения KeyboardInterrupt или SystemExit
        logger.error("Bot stopped!")
