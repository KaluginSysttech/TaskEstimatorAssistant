"""Точка входа приложения Telegram LLM Bot."""

import logging
import sys
from pathlib import Path

from dotenv import load_dotenv

from config.settings import Settings


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
    handlers = [
        # Вывод в консоль
        logging.StreamHandler(sys.stdout),
        # Запись всех логов в файл
        logging.FileHandler(logs_dir / "app.log", encoding="utf-8"),
        # Запись только ошибок в отдельный файл
        logging.FileHandler(logs_dir / "errors.log", encoding="utf-8"),
    ]
    
    # Фильтр для errors.log - только ERROR и выше
    handlers[2].setLevel(logging.ERROR)
    
    # Применение конфигурации
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format=log_format,
        handlers=handlers
    )


def main() -> None:
    """Точка входа приложения."""
    # Загрузка переменных окружения из .env
    load_dotenv()
    
    try:
        # Инициализация настроек с валидацией
        settings = Settings()
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


if __name__ == "__main__":
    main()

