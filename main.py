import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TOKEN
from utils import setup_logger

#установка логирования по умолчанию
#logging.basicConfig(level=logging.INFO)

#запуск логирования
setup_logger(fname=__name__)

#экземпляр бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

#бот принимает команды
@dp.message(Command('start'))
async def process_start_command(message):
    await message.answer("Привет!")
    logging.info(f"Пользователь с id={message.from_user.id} запустил бота")


@dp.message()
async def echo_message(message):
    await message.answer(message.text)
    logging.debug(f"Пользователь с id={message.from_user.id} прислал необрабатываемую команду")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
