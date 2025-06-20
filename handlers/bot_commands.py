

from aiogram.types import BotCommand
from aiogram import Bot


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Запускает бота"),
        BotCommand(command="/help", description="Выводит справочную информацию"),
        BotCommand(command="/status", description="Выводит статус пользователя"),
        BotCommand(command="/getres", description="Посмотреть задачи студентов"),
        BotCommand(command="/checked", description="Ваши задачи проверены преподавателем")

    ]
    await bot.set_my_commands(commands)