import pytest
from aiogram.types import InlineKeyboardMarkup
from fixtures import mock_message, mock_callback_query
from handlers.handlers import start_command, status_command, help_command, menu_command, echo_handler
from handlers.callbacks import send_random_value

@pytest.mark.asyncio
async def test_echo_handler(mock_message):
    mock_message.chat.id = 234243
    await echo_handler(mock_message)
    mock_message.send_copy.assert_awaited_once_with(chat_id=234243)

@pytest.mark.asyncio
async def test_start(mock_message):
    await start_command(mock_message)
    assert mock_message.answer.called, "message.answer не был вызван"
    called_args, called_kwargs = mock_message.answer.call_args
    assert called_args[0] == f"Выберите пункт меню:"
    markup = called_kwargs['reply_markup']
    assert isinstance(markup, InlineKeyboardMarkup), 'reply_markup не является Inline-клавиатурой'

@pytest.mark.asyncio
async def test_status(mock_message):
    await status_command(mock_message)
    assert mock_message.answer.called, "message.answer не был вызван"
    called_args, called_kwargs = mock_message.answer.call_args
    assert called_args[0] == f"Ваш ID: {mock_message.from_user.id}\nВаш username: @{mock_message.from_user.username}"

@pytest.mark.asyncio
async def test_help(mock_message):
    await help_command(mock_message)
    assert mock_message.answer.called, "message.answer не был вызван"
    called_args, called_kwargs = mock_message.answer.call_args
    assert called_args[0] == f"Список доступных команд:\n/start — запустить бота\n/status — проверить статус\n/help — помощь\n/menu — открыть меню"

@pytest.mark.asyncio
async def test_menu(mock_message):
    await menu_command(mock_message)
    assert mock_message.answer.called, "message.answer не был вызван"
    called_args, called_kwargs = mock_message.answer.call_args
    assert called_args[0] == f"Выберите пункт меню:"

import random
@pytest.mark.asyncio
async def test_button_message(mock_callback_query):
    await send_random_value(mock_callback_query)
    #random_number = random.randint(1, 100)
    #expected_message = f"Случайное значение: {random_number}"

    mock_callback_query.message.answer.assert_awaited_once()
