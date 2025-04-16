
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, types, html
import logging

from .keyboard import get_random_keyboard

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привет, {html.bold(message.from_user.full_name)}!")
    logging.info(f"user {message.from_user.id} starts bot")

@router.message(Command("status"))
async def command_status_handler(message: Message) -> None:
    await message.answer(f"username: {html.bold(message.from_user.username)}, id: {html.bold(message.from_user.id)}")
    logging.info(f"user {message.from_user.id} gets status")

@router.message(Command("help"))
async def command_help_handler(message: Message) -> None:
    help_text = """
Привет! Я бот. Вот список доступных команд:

/start - Запускает бота и выводит информацию о пользователе.
/help - Выводит справочную информацию о боте и доступных командах.
/status - Выводит ID и имя пользователя.
/random - Команда выводит кнопку ответ на нажатие которой - сообщение

Разработчики: @vvnniika, @possy_a
    """
    await message.answer(help_text)
    logging.info(f"user {message.from_user.id} gets help")

@router.message(Command("random"))
async def cmd_random(message: types.Message):
    keyboard = get_random_keyboard()
    await message.answer(
        "Нажмите на кнопку, чтобы бот отправил кое-что",
        reply_markup=keyboard
    )
    logging.info(f"user {message.from_user.id} gets random")

@router.message()
async def echo_handler(message: Message) -> None:
    try:
        await message.send_copy(chat_id=message.chat.id)
        logging.info(f"user {message.from_user.id} leaves unhandled message")
    except TypeError:
        await message.answer("Nice try!")
        logging.info(f"user {message.from_user.id} leaves unhandled message unsuccessfully")

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

