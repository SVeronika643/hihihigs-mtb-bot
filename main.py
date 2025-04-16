import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import BotCommand
from config import TOKEN

from handlers.handlers import router
from utils.logging import setup_logger  # Импорт логирования

# --- Включаем логирование ---
setup_logger(fname="bot")

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Функция установки команд ---
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="status", description="Проверить статус"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="random", description="Получить случайное значение"),
    ]
    await bot.set_my_commands(commands)

# Регистрируем команды
dp.startup.register(set_commands)

# Подключаем маршрутизаторы
dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
