"""Тесты для модуля управления историей диалогов."""

from llm.conversation import Conversation


def test_add_and_get_history() -> None:
    """Тест базовой работы: добавление и получение истории."""
    conv = Conversation(max_messages=10)

    # Добавляем сообщения
    conv.add_message(user_id=1, role="user", content="Hello")
    conv.add_message(user_id=1, role="assistant", content="Hi!")

    # Получаем историю
    history = conv.get_history(user_id=1)

    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[0]["content"] == "Hello"
    assert history[1]["role"] == "assistant"
    assert history[1]["content"] == "Hi!"


def test_history_limit() -> None:
    """Тест ограничения размера истории."""
    conv = Conversation(max_messages=3)

    # Добавляем больше сообщений, чем лимит
    conv.add_message(user_id=1, role="user", content="Msg 1")
    conv.add_message(user_id=1, role="assistant", content="Msg 2")
    conv.add_message(user_id=1, role="user", content="Msg 3")
    conv.add_message(user_id=1, role="assistant", content="Msg 4")

    # Проверяем, что осталось только последние 3
    history = conv.get_history(user_id=1)
    assert len(history) == 3
    assert history[0]["content"] == "Msg 2"


def test_different_users() -> None:
    """Тест изоляции истории между пользователями."""
    conv = Conversation()

    conv.add_message(user_id=1, role="user", content="User 1 message")
    conv.add_message(user_id=2, role="user", content="User 2 message")

    history1 = conv.get_history(user_id=1)
    history2 = conv.get_history(user_id=2)

    assert len(history1) == 1
    assert len(history2) == 1
    assert history1[0]["content"] != history2[0]["content"]


def test_clear_history() -> None:
    """Тест очистки истории."""
    conv = Conversation()

    conv.add_message(user_id=1, role="user", content="Test")
    assert len(conv.get_history(user_id=1)) == 1

    conv.clear_history(user_id=1)
    assert len(conv.get_history(user_id=1)) == 0


def test_clear_history_nonexistent_user() -> None:
    """Тест очистки истории для несуществующего пользователя."""
    conv = Conversation()

    # Не должно вызывать ошибку
    conv.clear_history(user_id=999)
    assert len(conv.get_history(user_id=999)) == 0


def test_get_stats() -> None:
    """Тест получения статистики."""
    conv = Conversation()

    conv.add_message(user_id=1, role="user", content="Test 1")
    conv.add_message(user_id=2, role="user", content="Test 2")
    conv.add_message(user_id=2, role="assistant", content="Response 2")

    stats = conv.get_stats()
    assert stats["total_users"] == 2
    assert stats["total_messages"] == 3


def test_get_stats_empty() -> None:
    """Тест статистики для пустого хранилища."""
    conv = Conversation()

    stats = conv.get_stats()
    assert stats["total_users"] == 0
    assert stats["total_messages"] == 0


def test_get_history_returns_copy() -> None:
    """Тест что get_history возвращает копию, а не оригинал."""
    conv = Conversation()

    conv.add_message(user_id=1, role="user", content="Original")
    history = conv.get_history(user_id=1)

    # Модифицируем полученную историю
    history.append({"role": "assistant", "content": "Modified"})

    # Проверяем, что оригинал не изменился
    original_history = conv.get_history(user_id=1)
    assert len(original_history) == 1
    assert original_history[0]["content"] == "Original"


def test_empty_history_for_new_user() -> None:
    """Тест получения истории для нового пользователя."""
    conv = Conversation()

    history = conv.get_history(user_id=999)
    assert len(history) == 0
    assert isinstance(history, list)
