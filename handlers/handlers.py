from aiogram import types, Router
from aiogram.filters import Command
from .keyboard import keyboard  # Импорт клавиатуры
from aiogram.types import Message

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

@router.message()
async def echo_handler(message: Message) -> None:

    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
        logging.info(f"user {message.from_user.id} leaves unhandled message")
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Nice try!")
        logging.info(f"user {message.from_user.id} leaves unhandled message unsuccessfully")