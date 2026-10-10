"""Клавиатуры и быстрые команды для бота."""

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Создаёт клавиатуру с командами для пользователя."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="/add"), KeyboardButton(text="/list")],
            [KeyboardButton(text="/list_csv")],
        ],
        resize_keyboard=True,
    )
    return keyboard
