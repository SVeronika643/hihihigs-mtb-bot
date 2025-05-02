import pytest
from main import main, set_commands
from aiogram.types import BotCommand
from unittest.mock import patch
from fixtures import mock_bot, mock_router, mock_set_commands, mock_setuplogger, mock_dispatcher

@pytest.mark.asyncio
async def test_main_initialization(mock_bot, mock_router, mock_set_commands, mock_setuplogger, mock_dispatcher):
    with patch(target="main.Bot", return_value=mock_bot), patch(target="main.Dispatcher", return_value=mock_dispatcher):
        await main()
        await set_commands(mock_bot)
        commands = [
            BotCommand(command="start", description="Запустить бота"),
            BotCommand(command="status", description="Проверить статус"),
            BotCommand(command="help", description="Помощь"),
        ]
        mock_setuplogger.assert_called_once()
        mock_dispatcher.startup.register.assert_called_once_with(mock_set_commands)
        mock_dispatcher.start_polling.assert_awaited_once_with(mock_bot)
        mock_dispatcher.include_router.assert_called_once()
        mock_bot.set_my_commands.assert_awaited_once_with(commands)
