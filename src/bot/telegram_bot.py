"""Основной класс Telegram бота."""

import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

from bot.message_handler import MessageHandler

logger = logging.getLogger(__name__)


class TelegramBot:
    """
    Основной класс Telegram бота.

    Отвечает за инициализацию aiogram компонентов,
    регистрацию handlers и запуск polling.
    """

    def __init__(self, token: str, message_handler: MessageHandler) -> None:
        """
        Инициализация бота.

        Args:
            token: Telegram Bot API токен
            message_handler: Обработчик сообщений и команд
        """
        self.bot = Bot(token=token)
        self.dp = Dispatcher()
        self.message_handler = message_handler

        # Регистрация handlers
        self._register_handlers()

        logger.info("TelegramBot initialized successfully")

    def _register_handlers(self) -> None:
        """Регистрация всех handlers в диспетчере."""
        # Команда /start
        self.dp.message.register(self.message_handler.handle_start, Command(commands=["start"]))

        # Команда /help
        self.dp.message.register(self.message_handler.handle_help, Command(commands=["help"]))

        # Команда /role
        self.dp.message.register(self.message_handler.handle_role, Command(commands=["role"]))

        # Текстовые сообщения (обрабатываются последними)
        self.dp.message.register(self.message_handler.handle_text)

        logger.info("All handlers registered")

    async def start(self) -> None:
        """Запуск бота в режиме long polling."""
        logger.info("Starting bot polling...")
        logger.info("Bot is ready to receive messages")

        try:
            # Удаляем webhook если он был установлен
            await self.bot.delete_webhook(drop_pending_updates=True)

            # Запускаем polling
            await self.dp.start_polling(self.bot)
        except Exception as e:
            logger.error(f"Error during polling: {e}")
            raise
        finally:
            await self.bot.session.close()
            logger.info("Bot stopped")

    async def stop(self) -> None:
        """Остановка бота."""
        logger.info("Stopping bot...")
        await self.dp.stop_polling()
        await self.bot.session.close()
        logger.info("Bot stopped successfully")
