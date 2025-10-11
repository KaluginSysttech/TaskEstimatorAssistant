"""Точка входа приложения Telegram LLM Bot."""

import asyncio
import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from bot import MessageHandler, TelegramBot
from config.settings import Settings
from llm import Conversation, LLMClient


def setup_logging(log_level: str) -> None:
    """
    Настройка логирования приложения.

    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
    """
    # Создаем директорию для логов, если её нет
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    # Формат сообщений
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Настройка handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = logging.FileHandler(logs_dir / "app.log", encoding="utf-8")
    error_handler = logging.FileHandler(logs_dir / "errors.log", encoding="utf-8")

    # Фильтр для errors.log - только ERROR и выше
    error_handler.setLevel(logging.ERROR)

    handlers: list[logging.Handler] = [console_handler, file_handler, error_handler]

    # Применение конфигурации
    logging.basicConfig(
        level=getattr(logging, log_level.upper()), format=log_format, handlers=handlers
    )


async def main() -> None:
    """Точка входа приложения."""
    # Загрузка переменных окружения из .env
    load_dotenv()

    try:
        # Инициализация настроек с валидацией
        settings = Settings()  # type: ignore[call-arg]
    except Exception as e:
        print(f"Ошибка загрузки конфигурации: {e}")
        print("Убедитесь, что файл .env создан и содержит все обязательные параметры.")
        print("Пример можно найти в .env.example")
        sys.exit(1)

    # Настройка логирования
    setup_logging(settings.log_level)
    logger = logging.getLogger(__name__)

    logger.info("=" * 50)
    logger.info("Starting Telegram LLM Bot")
    logger.info("=" * 50)
    logger.info(f"Using LLM model: {settings.openrouter_model}")
    logger.info(f"Max history messages: {settings.max_history_messages}")
    logger.info(f"LLM timeout: {settings.llm_timeout}s")
    logger.info(f"Log level: {settings.log_level}")
    logger.info("Configuration loaded successfully")
    logger.info("=" * 50)

    # Инициализация компонентов
    llm_client = LLMClient(
        api_key=settings.openrouter_api_key,
        model=settings.openrouter_model,
        timeout=settings.llm_timeout,
    )

    conversation = Conversation(max_messages=settings.max_history_messages)

    message_handler = MessageHandler(llm_client=llm_client, conversation=conversation)

    telegram_bot = TelegramBot(token=settings.telegram_bot_token, message_handler=message_handler)

    # Запуск бота
    try:
        await telegram_bot.start()
    except KeyboardInterrupt:
        logger.info("Received interrupt signal")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        logger.info("Shutting down gracefully...")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)
