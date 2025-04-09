from aiogram import types, Router
from aiogram.filters import Command
from .keyboard import keyboard  # Импорт клавиатуры

# Создаём экземпляр Router
router = Router()

@router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Выберите пункт меню:", reply_markup=keyboard)

@router.message(Command("status"))
async def status_command(message: types.Message):
    await message.answer(f"Ваш ID: {message.from_user.id}\nВаш username: @{message.from_user.username}")

@router.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer("Список доступных команд:\n/start — запустить бота\n/status — проверить статус\n/help — помощь\n/menu — открыть меню")

@router.message(Command("menu"))
async def menu_command(message: types.Message):
    await message.answer("Выберите пункт меню:", reply_markup=keyboard)