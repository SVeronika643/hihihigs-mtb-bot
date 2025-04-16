import logging
import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import BotCommand
from config import TOKEN


from handlers import router, send_random_value
from handlers.keyboard import get_random_keyboard

from utils import setup_logger


from handlers.handlers import router
from utils.logging import setup_logger  # Импорт логирования

# --- Включаем логирование ---
setup_logger(fname="bot")



dp = Dispatcher()



#бот принимает команды
@dp.message(Command('start'))
async def process_start_command(message):
    await message.answer("Привет!")
    logging.info(f"Пользователь с id={message.from_user.id} запустил бота")

# Создаём бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Функция установки команд ---
async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="status", description="Проверить статус"),
        BotCommand(command="help", description="Помощь"),
    ]
    await bot.set_my_commands(commands)


# Регистрируем команды
dp.startup.register(set_commands)


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="status", description="Проверить статус"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="random", description="Получить случайное значение"),
    ]
    await bot.set_my_commands(commands)



@dp.message()
async def echo_message(message):
    await message.answer(message.text)
    logging.debug(f"Пользователь с id={message.from_user.id} прислал необрабатываемую команду")


async def main() -> None:
    bot = Bot(token=TOKEN)
    dp.include_router(router)
    dp.startup.register(lambda: set_commands(bot))

    # Регистрируем обработчик callback
    dp.callback_query.register(send_random_value, lambda c: c.data == "random_value")


# Подключаем маршрутизаторы
dp.include_router(router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
