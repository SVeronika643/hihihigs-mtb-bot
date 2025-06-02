from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

def keyboard() -> types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="кнопка",
        callback_data="random_value")
    )
    return builder.as_markup()

button_tutor = InlineKeyboardButton(text="Преподаватель", callback_data="button_tutor")
button_student = InlineKeyboardButton(text="Слушатель", callback_data="button_student")

keyboard_start = InlineKeyboardMarkup(inline_keyboard=[[button_tutor, button_student]])