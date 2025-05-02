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

@pytest.fixture
def mock_message():
    mock_msg = AsyncMock(spec=Message)
    mock_msg.from_user = AsyncMock()
    mock_msg.from_user.id = AsyncMock()
    mock_msg.from_user.username = AsyncMock()
    mock_msg.answer = AsyncMock()
    mock_msg.chat = AsyncMock()
    mock_msg.send_copy = AsyncMock()

    return mock_msg

@pytest.fixture
def mock_callback_query():
    mock = MagicMock(spec=CallbackQuery)
    mock.data = "button_callback"
    mock.message = MagicMock()
    mock.message.answer = AsyncMock()
    mock.from_user = MagicMock()
    mock.from_user.username = "test_user"
    
    return mock

@pytest.fixture
def mock_c_router():
    return MagicMock()

@pytest.fixture
def mock_h_router():
    return MagicMock()
