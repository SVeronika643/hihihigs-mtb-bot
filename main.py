import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config import TOKEN
from handlers import router, send_random_value
from handlers.keyboard import get_random_keyboard

dp = Dispatcher()


async def set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="status", description="Проверить статус"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command="random", description="Получить случайное значение"),
    ]
    await bot.set_my_commands(commands)


async def main() -> None:
    bot = Bot(token=TOKEN)
    dp.include_router(router)
    dp.startup.register(lambda: set_commands(bot))

    # Регистрируем обработчик callback
    dp.callback_query.register(send_random_value, lambda c: c.data == "random_value")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())