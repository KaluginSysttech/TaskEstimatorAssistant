"""Обработчик сообщений и команд Telegram бота."""

import logging
from typing import Optional

from aiogram import types
from aiogram.filters import Command


logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Обработчик сообщений и команд бота.
    
    Содержит handlers для команд /start, /help и текстовых сообщений.
    Интегрирован с LLM для обработки пользовательских запросов.
    """
    
    def __init__(
        self, 
        llm_client: Optional['LLMClient'] = None,
        conversation: Optional['Conversation'] = None
    ) -> None:
        """
        Инициализация обработчика.
        
        Args:
            llm_client: Клиент для работы с LLM (опционально для обратной совместимости)
            conversation: Хранилище истории диалогов
        """
        self.llm_client = llm_client
        self.conversation = conversation
        logger.info("MessageHandler initialized")
    
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
        Обработка текстовых сообщений через LLM.
        
        Отправляет сообщение пользователя в LLM и возвращает ответ.
        Если LLM не настроен, работает в echo режиме.
        
        Args:
            message: Входящее сообщение от пользователя
        """
        user_id = message.from_user.id
        text = message.text
        
        logger.info(f"Received message from user {user_id}: {text}")
        
        # Проверяем наличие LLM клиента
        if self.llm_client is None:
            # Fallback: echo режим
            response = f"📝 Вы написали: {text}"
            await message.answer(response)
            logger.info(f"Sent echo response to user {user_id} (LLM not configured)")
            return
        
        try:
            # Получаем историю диалога, если есть Conversation
            history = []
            if self.conversation:
                history = self.conversation.get_history(user_id)
                logger.info(f"Retrieved history for user {user_id}: {len(history)} messages")
            
            # Отправляем запрос в LLM с историей
            logger.info(f"Sending user message to LLM")
            response = await self.llm_client.get_response(text, history=history)
            
            # Сохраняем пару вопрос-ответ в историю
            if self.conversation:
                self.conversation.add_message(user_id, "user", text)
                self.conversation.add_message(user_id, "assistant", response)
                logger.info(f"Saved user-assistant pair to history for user {user_id}")
            
            # Разбиваем длинные ответы на части (лимит Telegram: 4096 символов)
            max_length = 4000  # Оставляем запас
            if len(response) <= max_length:
                await message.answer(response)
            else:
                # Разбиваем на части
                parts = []
                while response:
                    if len(response) <= max_length:
                        parts.append(response)
                        break
                    
                    # Ищем последний перенос строки в пределах лимита
                    split_pos = response.rfind('\n', 0, max_length)
                    if split_pos == -1:
                        # Если нет переносов, режем по словам
                        split_pos = response.rfind(' ', 0, max_length)
                    if split_pos == -1:
                        # В крайнем случае режем по символам
                        split_pos = max_length
                    
                    parts.append(response[:split_pos])
                    response = response[split_pos:].lstrip()
                
                # Отправляем все части
                for i, part in enumerate(parts, 1):
                    if len(parts) > 1:
                        prefix = f"[Часть {i}/{len(parts)}]\n\n"
                        await message.answer(prefix + part)
                    else:
                        await message.answer(part)
            
            logger.info(f"Sent LLM response to user {user_id}")
            
        except Exception as e:
            # Обработка ошибок LLM
            error_message = (
                "😔 Извините, произошла ошибка при обработке вашего запроса. "
                "Пожалуйста, попробуйте позже."
            )
            await message.answer(error_message)
            logger.error(f"Failed to get LLM response for user {user_id}: {e}")

