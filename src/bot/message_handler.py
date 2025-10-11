"""Обработчик сообщений и команд Telegram бота."""

import logging
from typing import TYPE_CHECKING

from aiogram import types

if TYPE_CHECKING:
    from src.llm.conversation import Conversation
    from src.llm.llm_client import LLMClient

logger = logging.getLogger(__name__)


class MessageHandler:
    """
    Обработчик сообщений и команд бота.

    Содержит handlers для команд /start, /help и текстовых сообщений.
    Интегрирован с LLM для обработки пользовательских запросов.
    """

    def __init__(
        self,
        llm_client: "LLMClient",
        conversation: "Conversation",
    ) -> None:
        """
        Инициализация обработчика.

        Args:
            llm_client: Клиент для работы с LLM (обязательный)
            conversation: Хранилище истории диалогов (обязательное)
        """
        self.llm_client = llm_client
        self.conversation = conversation
        logger.info("MessageHandler initialized")

    def _split_message(self, text: str, max_length: int) -> list[str]:
        """
        Разбить длинное сообщение на части для отправки в Telegram.

        Разбивка происходит с приоритетом:
        1. По переносу строки (\\n)
        2. По пробелу (слова)
        3. По символам (если нет другого варианта)

        Args:
            text: Текст для разбивки
            max_length: Максимальная длина одной части

        Returns:
            Список частей сообщения

        Examples:
            >>> handler._split_message("Short text", 100)
            ["Short text"]

            >>> handler._split_message("Very long text...", 10)
            ["Very long", "text..."]
        """
        if len(text) <= max_length:
            return [text]

        parts = []
        remaining = text

        while remaining:
            if len(remaining) <= max_length:
                parts.append(remaining)
                break

            # Ищем последний перенос строки в пределах лимита
            split_pos = remaining.rfind("\n", 0, max_length)
            if split_pos == -1:
                # Если нет переносов, режем по словам
                split_pos = remaining.rfind(" ", 0, max_length)
            if split_pos == -1:
                # В крайнем случае режем по символам
                split_pos = max_length

            parts.append(remaining[:split_pos])
            remaining = remaining[split_pos:].lstrip()

        logger.debug(f"Split message into {len(parts)} parts")
        return parts

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
            "👋 <b>Привет! Я помощник по оценке задач.</b>\n\n"
            "🎯 <b>Моя задача:</b>\n"
            "Помочь вам определить три ключевые величины для вашей задачи:\n"
            "• <b>СЛОЖНОСТЬ</b> - насколько задача сложна в реализации\n"
            "• <b>НЕОПРЕДЕЛЕННОСТЬ</b> - насколько понятны требования\n"
            "• <b>ОБЪЕМ</b> - сколько работы требуется\n\n"
            "💡 <b>Как я работаю:</b>\n"
            "Я буду задавать вам наводящие вопросы о вашем восприятии задачи.\n"
            "Мне не нужно знать суть задачи - важно ваше мнение о её характеристиках.\n\n"
            "📖 Используйте /help для подробной справки."
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
            "📖 <b>Справка по использованию</b>\n\n"
            "🤖 <b>Доступные команды:</b>\n"
            "/start - Приветственное сообщение\n"
            "/help - Эта справка\n\n"
            "🎯 <b>Что я оцениваю:</b>\n"
            "Я помогаю определить три величины для вашей задачи:\n"
            "1. <b>СЛОЖНОСТЬ</b> - насколько задача сложна в реализации\n"
            "2. <b>НЕОПРЕДЕЛЕННОСТЬ</b> - насколько понятны требования и подходы\n"
            "3. <b>ОБЪЕМ</b> - сколько работы требуется для выполнения\n\n"
            "💡 <b>Как это работает:</b>\n"
            "• Вы начинаете диалог с любого сообщения о задаче\n"
            "• Я задаю вам наводящие вопросы о вашем восприятии\n"
            "• Отвечайте на вопросы исходя из вашего понимания задачи\n"
            "• Когда информации достаточно, я помогу сформулировать оценку\n\n"
            "⚠️ <b>Важно:</b>\n"
            "Мне не нужно знать техническую суть вашей задачи.\n"
            "Я анализирую только ваши ответы и помогаю структурировать оценку.\n\n"
            "💬 <b>Контекст диалога:</b>\n"
            "Я помню последние 10 пар вопрос-ответ, поэтому диалог будет последовательным.\n\n"
            "🎯 <b>Пример диалога:</b>\n"
            'Вы: "Мне нужно оценить задачу"\n'
            'Я: "Насколько понятно вам, что именно нужно сделать?"\n'
            'Вы: "В целом понятно, но есть несколько неясных моментов"\n'
            'Я: "Как вы оцениваете сложность реализации?" (и так далее)'
        )

        await message.answer(help_text, parse_mode="HTML")
        logger.info(f"Sent help message to user {user_id}")

    async def handle_text(self, message: types.Message) -> None:
        """
        Обработка текстовых сообщений через LLM.

        Отправляет сообщение пользователя в LLM и возвращает ответ.

        Args:
            message: Входящее сообщение от пользователя
        """
        user_id = message.from_user.id
        text = message.text

        logger.info(f"Received message from user {user_id}: {text}")

        try:
            # Получаем историю диалога
            history = self.conversation.get_history(user_id)
            logger.info(f"Retrieved history for user {user_id}: {len(history)} messages")

            # Отправляем запрос в LLM с историей
            logger.info("Sending user message to LLM")
            response = await self.llm_client.get_response(text, history=history)

            # Сохраняем пару вопрос-ответ в историю
            self.conversation.add_message(user_id, "user", text)
            self.conversation.add_message(user_id, "assistant", response)
            logger.info(f"Saved user-assistant pair to history for user {user_id}")

            # Разбиваем длинные ответы на части (лимит Telegram: 4096 символов)
            max_length = 4000  # Оставляем запас
            parts = self._split_message(response, max_length)

            # Отправляем все части
            for i, part in enumerate(parts, 1):
                if len(parts) > 1:
                    prefix = f"[Часть {i}/{len(parts)}]\n\n"
                    await message.answer(prefix + part)
                else:
                    await message.answer(part)

            logger.info(f"Sent LLM response to user {user_id}")

        except TimeoutError as e:
            # Таймаут запроса
            error_message = (
                "⏱️ Превышено время ожидания ответа. "
                "Пожалуйста, попробуйте задать вопрос короче или повторите попытку позже."
            )
            await message.answer(error_message)
            logger.error(f"Timeout getting LLM response for user {user_id}: {e}")

        except ConnectionError as e:
            # Ошибка сети
            error_message = "🌐 Проблемы с подключением к серверу. Пожалуйста, попробуйте позже."
            await message.answer(error_message)
            logger.error(f"Connection error for user {user_id}: {e}")

        except ValueError as e:
            # Rate limit
            error_message = (
                "⚠️ Превышен лимит запросов. Пожалуйста, подождите немного и попробуйте снова."
            )
            await message.answer(error_message)
            logger.error(f"Rate limit error for user {user_id}: {e}")

        except RuntimeError as e:
            # API ошибки
            error_message = "❌ Ошибка сервера обработки запросов. Пожалуйста, попробуйте позже."
            await message.answer(error_message)
            logger.error(f"API error for user {user_id}: {e}")

        except Exception as e:
            # Неожиданные ошибки
            error_message = "😔 Произошла непредвиденная ошибка. Пожалуйста, попробуйте позже."
            await message.answer(error_message)
            logger.error(f"Unexpected error for user {user_id}: {e}", exc_info=True)
