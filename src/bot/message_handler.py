"""Обработчик сообщений и команд Telegram бота."""

import logging
from aiogram import types
from aiogram.filters import Command


logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Обработчик сообщений и команд бота.
    
    Содержит handlers для команд /start, /help и текстовых сообщений.
    В текущей версии работает в режиме echo (дублирует сообщения).
    """
    
    async def handle_start(self, message: types.Message) -> None:
        """
        Обработка команды /start.
        
        Args:
            message: Входящее сообщение от пользователя
        """
        user_id = message.from_user.id
        username = message.from_user.username or "пользователь"
        
        logger.info(f"User {user_id} (@{username}) started the bot")
        
        welcome_text = (
            "👋 <b>Привет! Я бот для оценки IT задач.</b>\n\n"
            "Я помогу тебе оценить сложность и трудоёмкость задач.\n\n"
            "Просто отправь мне описание задачи, и я дам свою оценку.\n\n"
            "Используй /help для получения справки."
        )
        
        await message.answer(welcome_text, parse_mode="HTML")
        logger.info(f"Sent welcome message to user {user_id}")
    
    async def handle_help(self, message: types.Message) -> None:
        """
        Обработка команды /help.
        
        Args:
            message: Входящее сообщение от пользователя
        """
        user_id = message.from_user.id
        logger.info(f"User {user_id} requested help")
        
        help_text = (
            "📖 <b>Доступные команды:</b>\n\n"
            "/start - Начать работу с ботом\n"
            "/help - Показать эту справку\n\n"
            "<b>Как пользоваться:</b>\n"
            "Просто отправь мне текстовое описание задачи, "
            "и я помогу оценить её сложность и трудоёмкость.\n\n"
            "<b>Пример:</b>\n"
            "<i>\"Создать REST API для управления пользователями с аутентификацией\"</i>"
        )
        
        await message.answer(help_text, parse_mode="HTML")
        logger.info(f"Sent help message to user {user_id}")
    
    async def handle_text(self, message: types.Message) -> None:
        """
        Обработка текстовых сообщений (echo режим).
        
        В текущей версии просто дублирует сообщение обратно пользователю.
        В следующих итерациях будет заменено на отправку в LLM.
        
        Args:
            message: Входящее сообщение от пользователя
        """
        user_id = message.from_user.id
        text = message.text
        
        logger.info(f"Received message from user {user_id}: {text}")
        
        # Echo режим - дублируем сообщение
        response = f"📝 Вы написали: {text}"
        
        await message.answer(response)
        logger.info(f"Sent echo response to user {user_id}")

