from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types

def keyboard():
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(text="📖 О нас",callback_data="button"))
    return builder.as_markup()
