import pytest
from aiogram.types import Message, CallbackQuery
from aiogram import Router, Dispatcher, Bot
from unittest.mock import MagicMock, AsyncMock, Mock, patch

@pytest.fixture
def mock_bot():
    return AsyncMock(spec=Bot)

@pytest.fixture
def mock_router():
    return Mock(spec=Router)

@pytest.fixture
def mock_set_commands():
    with patch(target="main.set_commands", new_callable=AsyncMock) as mock:
        yield mock

@pytest.fixture
def mock_setuplogger():
    with patch("main.setup_logger") as mock:
        yield mock

@pytest.fixture
def mock_dispatcher():
    mock = MagicMock(spec=Dispatcher)
    mock.start_polling = AsyncMock()
    mock.startup = MagicMock()
    mock.startup.register = MagicMock()
    mock.include_router = MagicMock()

    return mock
