"""Тесты для обработчика сообщений."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from bot.message_handler import MessageHandler


@pytest.fixture
def mock_llm_client() -> MagicMock:
    """Фикстура с мок LLM клиента."""
    client = MagicMock()
    client.system_prompt = (
        "Ты помощник по оценке задач. "
        "Твоя роль - помогать пользователю определить три ключевые величины для задачи:\n"
        "1. СЛОЖНОСТЬ - насколько задача сложна в реализации\n"
        "2. НЕОПРЕДЕЛЕННОСТЬ - насколько понятны требования и подходы к решению\n"
        "3. ОБЪЕМ - сколько работы требуется для выполнения"
    )
    return client


@pytest.fixture
def mock_conversation() -> MagicMock:
    """Фикстура с мок хранилищем диалогов."""
    return MagicMock()


@pytest.fixture
def message_handler(mock_llm_client: MagicMock, mock_conversation: MagicMock) -> MessageHandler:
    """Фикстура с MessageHandler."""
    return MessageHandler(llm_client=mock_llm_client, conversation=mock_conversation)


async def test_handle_role_displays_prompt(message_handler: MessageHandler) -> None:
    """Тест отображения роли ассистента командой /role."""
    # Arrange: создаем мок сообщения
    message = AsyncMock()
    message.from_user = MagicMock(id=123, username="testuser")
    message.answer = AsyncMock()

    # Act: вызываем обработчик
    await message_handler.handle_role(message)

    # Assert: проверяем что ответ содержит информацию о роли
    message.answer.assert_called_once()
    call_args = message.answer.call_args
    response_text = call_args[0][0]

    assert "🎭" in response_text
    assert "Моя роль" in response_text or "роль" in response_text.lower()
    assert "оценк" in response_text.lower()


async def test_handle_role_contains_key_info(message_handler: MessageHandler) -> None:
    """Тест что /role содержит ключевую информацию из системного промпта."""
    # Arrange
    message = AsyncMock()
    message.from_user = MagicMock(id=123, username="testuser")
    message.answer = AsyncMock()

    # Act
    await message_handler.handle_role(message)

    # Assert
    call_args = message.answer.call_args
    response_text = call_args[0][0]

    # Проверяем что в ответе есть упоминание трех величин
    assert "СЛОЖНОСТЬ" in response_text or "сложност" in response_text.lower()
    assert "НЕОПРЕДЕЛЕННОСТЬ" in response_text or "неопределенност" in response_text.lower()
    assert "ОБЪЕМ" in response_text or "объем" in response_text.lower()


async def test_handle_role_without_user(message_handler: MessageHandler) -> None:
    """Тест обработки /role без информации о пользователе."""
    # Arrange: сообщение без from_user
    message = AsyncMock()
    message.from_user = None
    message.answer = AsyncMock()

    # Act: вызываем обработчик
    await message_handler.handle_role(message)

    # Assert: ответ не должен быть отправлен
    message.answer.assert_not_called()


async def test_handle_role_uses_html_parse_mode(message_handler: MessageHandler) -> None:
    """Тест что /role использует HTML форматирование."""
    # Arrange
    message = AsyncMock()
    message.from_user = MagicMock(id=123, username="testuser")
    message.answer = AsyncMock()

    # Act
    await message_handler.handle_role(message)

    # Assert: проверяем что используется parse_mode="HTML"
    message.answer.assert_called_once()
    call_kwargs = message.answer.call_args[1]
    assert call_kwargs.get("parse_mode") == "HTML"
