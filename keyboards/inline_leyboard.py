from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from lexicon.lexicon import LEXICON


def create_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    # Создаем билдер (строитель) клавиатуры
    builder = InlineKeyboardBuilder()
    
    # Добавляем в билдер ряд с кнопками
    builder.row(*[InlineKeyboardButton(
            text=LEXICON[button] if button in LEXICON else button,
            callback_data=button) for button in buttons])
    
    # возвращаем объект клавиатуры
    return builder.as_markup()