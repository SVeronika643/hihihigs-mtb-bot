

from aiogram.types import BotCommand
from aiogram import Bot


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Запускает бота"),
        BotCommand(command="/help", description="Выводит справочную информацию"),
        BotCommand(command="/status", description="Выводит статус пользователя"),
        BotCommand(command="/load", description="Загружает ссылки")

    ]
    await bot.set_my_commands(commands)