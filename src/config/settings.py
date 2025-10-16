"""Конфигурация приложения."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Конфигурация приложения с валидацией через Pydantic.

    Загружает настройки из переменных окружения или .env файла.
    Fail-fast при отсутствии обязательных параметров.
    """

    # Telegram
    telegram_bot_token: str = Field(..., description="Telegram Bot API токен")

    # OpenRouter
    openrouter_api_key: str = Field(..., description="OpenRouter API ключ")
    openrouter_model: str = Field(
        default="openai/gpt-3.5-turbo", description="Модель LLM для использования"
    )

    # Database
    database_url: str = Field(
        default="postgresql+asyncpg://telegrambot:telegrambot_password@localhost:5432/telegrambot",
        description="URL подключения к PostgreSQL",
    )

    # Application
    max_history_messages: int = Field(
        default=20, description="Максимальное количество сообщений в истории диалога"
    )
    llm_timeout: int = Field(default=30, description="Таймаут запроса к LLM в секундах")
    log_level: str = Field(
        default="INFO", description="Уровень логирования (DEBUG, INFO, WARNING, ERROR)"
    )
    telegram_message_max_length: int = Field(
        default=4000, description="Максимальная длина сообщения Telegram (с запасом от 4096)"
    )

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )
