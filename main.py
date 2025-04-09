import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import BotCommand
from config import TOKEN

from handlers.handlers import router as handlers_router
from handlers.bot_commands import set_commands

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Подключаем маршрутизаторы
dp.include_router(handlers_router)

# Регистрируем команды
dp.startup.register(set_commands)

# Запуск бота
async def main():
    await dp.start_polling(bot)

# Правильная проверка запуска
if __name__ == "__main__":
    asyncio.run(main())