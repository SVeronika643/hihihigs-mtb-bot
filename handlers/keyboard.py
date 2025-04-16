from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Список кнопок для клавиатуры
kb_list = [
    [KeyboardButton(text="📖 О нас"),]
]

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(keyboard=kb_list, resize_keyboard=True, one_time_keyboard=True)

# Экспортируем переменную keyboard
all = ['keyboard']