import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import BotCommand
from handlers import handlers, callbacks
from config import TOKEN
from db import async_create_table
from handlers.handlers import router as handlers_router
from handlers.callbacks import router as callbacks_router
from utils.logging import setup_logger  # Импорт логирования

# --- Функция установки команд ---
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="status", description="Проверить статус"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command='load',description="Загрузить задачи"),
        BotCommand(command='getres', description="Посмотреть задачи студентов"),
        BotCommand(command="checked", description="Ваши задачи проверены преподавателем!")

    ]
    await bot.set_my_commands(commands)

# Запуск бота
async def main():

    # --- Включаем логирование ---
    setup_logger(fname="bot")

    # Создаём бота и диспетчер
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    # Регистрируем команды
    dp.startup.register(set_commands)

    # Подключаем маршрутизаторы
    dp.include_router(handlers_router)
    dp.include_router(callbacks_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(async_create_table())
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("End Script")
