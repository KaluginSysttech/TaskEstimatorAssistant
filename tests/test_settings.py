"""Тесты для модуля конфигурации."""

import pytest
from pydantic import ValidationError

from config.settings import Settings


def test_settings_with_required_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест загрузки настроек с обязательными полями."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token_123")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key_456")

    settings = Settings()  # type: ignore[call-arg]

    assert settings.telegram_bot_token == "test_token_123"
    assert settings.openrouter_api_key == "test_key_456"


def test_settings_default_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест значений по умолчанию."""
    # Устанавливаем только обязательные поля
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    # Удаляем опциональные поля, чтобы проверить дефолты
    monkeypatch.delenv("OPENROUTER_MODEL", raising=False)
    monkeypatch.delenv("MAX_HISTORY_MESSAGES", raising=False)
    monkeypatch.delenv("LLM_TIMEOUT", raising=False)
    monkeypatch.delenv("LOG_LEVEL", raising=False)
    monkeypatch.delenv("TELEGRAM_MESSAGE_MAX_LENGTH", raising=False)

    settings = Settings()  # type: ignore[call-arg]

    # Проверяем дефолтные значения
    assert settings.max_history_messages == 20
    assert settings.llm_timeout == 30
    assert settings.log_level == "INFO"
    assert settings.telegram_message_max_length == 4000


def test_settings_custom_values(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест кастомных значений."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "key")
    monkeypatch.setenv("OPENROUTER_MODEL", "gpt-4")
    monkeypatch.setenv("MAX_HISTORY_MESSAGES", "50")
    monkeypatch.setenv("LLM_TIMEOUT", "60")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("TELEGRAM_MESSAGE_MAX_LENGTH", "3000")

    settings = Settings()  # type: ignore[call-arg]

    assert settings.openrouter_model == "gpt-4"
    assert settings.max_history_messages == 50
    assert settings.llm_timeout == 60
    assert settings.log_level == "DEBUG"
    assert settings.telegram_message_max_length == 3000


def test_settings_missing_telegram_token(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест fail-fast при отсутствии TELEGRAM_BOT_TOKEN."""
    # Отключаем загрузку из .env файла
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    # Убираем TELEGRAM_BOT_TOKEN
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    # Отключаем загрузку из .env файла через pydantic
    monkeypatch.setattr("config.settings.Settings.model_config", {"env_file": None})

    with pytest.raises(ValidationError) as exc_info:
        Settings()  # type: ignore[call-arg]

    # Проверяем, что ошибка содержит информацию о пропущенном поле
    assert "telegram_bot_token" in str(exc_info.value).lower()


def test_settings_missing_openrouter_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест fail-fast при отсутствии OPENROUTER_API_KEY."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "test_token")
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    # Отключаем загрузку из .env файла через pydantic
    monkeypatch.setattr("config.settings.Settings.model_config", {"env_file": None})

    with pytest.raises(ValidationError) as exc_info:
        Settings()  # type: ignore[call-arg]

    # Проверяем, что ошибка содержит информацию о пропущенном поле
    assert "openrouter_api_key" in str(exc_info.value).lower()


def test_settings_missing_both_required_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест fail-fast при отсутствии всех обязательных полей."""
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    # Отключаем загрузку из .env файла через pydantic
    monkeypatch.setattr("config.settings.Settings.model_config", {"env_file": None})

    with pytest.raises(ValidationError) as exc_info:
        Settings()  # type: ignore[call-arg]

    error_str = str(exc_info.value).lower()
    assert "telegram_bot_token" in error_str
    assert "openrouter_api_key" in error_str


def test_settings_integer_fields_validation(monkeypatch: pytest.MonkeyPatch) -> None:
    """Тест валидации числовых полей."""
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "token")
    monkeypatch.setenv("OPENROUTER_API_KEY", "key")
    monkeypatch.setenv("MAX_HISTORY_MESSAGES", "100")
    monkeypatch.setenv("LLM_TIMEOUT", "120")

    settings = Settings()  # type: ignore[call-arg]

    assert isinstance(settings.max_history_messages, int)
    assert isinstance(settings.llm_timeout, int)
    assert isinstance(settings.telegram_message_max_length, int)
    assert settings.max_history_messages == 100
    assert settings.llm_timeout == 120
