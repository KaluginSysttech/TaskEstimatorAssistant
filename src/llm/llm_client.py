"""Клиент для работы с LLM через OpenRouter."""

import logging
from typing import List, Dict

from openai import AsyncOpenAI


logger = logging.getLogger(__name__)


class LLMClient:
    """
    Клиент для работы с LLM через OpenRouter API.
    
    Использует OpenAI-совместимый API для отправки запросов к LLM.
    Системный промпт жестко закодирован для оценки IT задач.
    """
    
    # Системный промпт для оценки задач
    SYSTEM_PROMPT = "Ты помощник для оценивания задач для IT сотрудников"
    
    def __init__(self, api_key: str, model: str, timeout: int) -> None:
        """
        Инициализация LLM клиента.
        
        Args:
            api_key: API ключ для OpenRouter
            model: Название модели для использования
            timeout: Таймаут запроса в секундах
        """
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
            timeout=timeout
        )
        self.model = model
        self.timeout = timeout
        
        logger.info(f"LLMClient initialized with model: {model}")
    
    async def get_response(self, user_message: str) -> str:
        """
        Получить ответ от LLM без истории диалога.
        
        Отправляет одиночный запрос с системным промптом.
        В следующих итерациях будет добавлена поддержка истории.
        
        Args:
            user_message: Сообщение от пользователя
            
        Returns:
            Ответ от LLM
            
        Raises:
            Exception: При ошибках API или таймауте
        """
        logger.info(f"Sending request to LLM (model: {self.model})")
        logger.debug(f"User message: {user_message}")
        
        try:
            # Формируем запрос с системным промптом
            messages = [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ]
            
            # Отправляем запрос
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )
            
            # Извлекаем ответ
            assistant_message = response.choices[0].message.content
            
            logger.info("Successfully received response from LLM")
            logger.debug(f"Assistant response: {assistant_message}")
            
            return assistant_message
            
        except Exception as e:
            logger.error(f"Error getting LLM response: {e}", exc_info=True)
            raise

