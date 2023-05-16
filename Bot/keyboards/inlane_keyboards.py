from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_kb(width: int,
                     last_btn: str | None = None,
                     **kwargs: [str, str]) -> InlineKeyboardMarkup:
    """
    Генератор инлайн-клавиатуры
    На вход принимает параметр width, именованные параметры (ключи/значения)
    из которых можно сформировать инлайн-кнопки. Ключ - это название кнопки,
    значение - data. Функция при необходимости добавляет последнюю кнопку,
    если передан аргумент last_btn.
    Возвращает объект инлайн-клавиатуры.
    """
    # Инициализация билдера
    kb_builder = InlineKeyboardBuilder()
    # Инициализация списка для кнопок
    buttons = []

    # Заполняем список кнопками из kwargs
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=button,
                callback_data=text))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=width)

    # Добавляем в билдер последнюю кнопку, если она передана в функцию
    if last_btn:
        kb_builder.row(InlineKeyboardButton(
            text=last_btn,
            callback_data='last_btn'))

    return kb_builder.as_markup()


######################################################################################################

def kb_inline_days():
    """
    Клавиатура выбора числа месяца
    """
    # Инициализация билдера
    kb_builder = InlineKeyboardBuilder()

    # Инициализация списка для кнопок
    buttons = []

    date_dict = {x: x for x in range(1, 32)}

    for button, data in date_dict.items():
        buttons.append(InlineKeyboardButton(
            text=button,
            callback_data=data))

    # Распаковываем список с кнопками в билдер методом row c параметром width
    kb_builder.row(*buttons, width=7)

    return kb_builder.as_markup()
