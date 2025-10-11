"""Клиент для работы с LLM через OpenRouter."""

import logging
import time

from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncOpenAI, RateLimitError

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Клиент для работы с LLM через OpenRouter API.

    Использует OpenAI-совместимый API для отправки запросов к LLM.
    Системный промпт жестко закодирован для оценки IT задач.
    """

    # Системный промпт для оценки задач
    SYSTEM_PROMPT = """Ты помощник по оценке задач. \
Твоя роль - помогать пользователю определить три ключевые величины для задачи:
1. СЛОЖНОСТЬ - насколько задача сложна в реализации
2. НЕОПРЕДЕЛЕННОСТЬ - насколько понятны требования и подходы к решению
3. ОБЪЕМ - сколько работы требуется для выполнения

ВАЖНЫЕ ПРАВИЛА:
- Ты НЕ должен знать или понимать суть задачи, которую оценивает пользователь
- Ты НЕ должен пытаться понять техническую суть или детали задачи
- Ты анализируешь ТОЛЬКО ответы пользователя, а не саму задачу
- Твоя цель - задавать наводящие вопросы, чтобы получить достаточно информации \
для оценки трех величин

Твой подход:
1. Задавай вопросы о том, как пользователь видит сложность, неопределенность и объем
2. Не спрашивай про технические детали задачи
3. Фокусируйся на восприятии пользователя, а не на объективных характеристиках задачи
4. Когда информации достаточно, помогай сформулировать итоговую оценку по трем величинам

Примеры хороших вопросов:
- "Насколько понятно вам, что именно нужно сделать?"
- "Есть ли неясности в требованиях или подходе к решению?"
- "Как вы оцениваете сложность реализации - высокая, средняя или низкая?"
- "Сколько времени, по вашим ощущениям, может занять эта работа?"

Помни контекст диалога для более эффективной помощи в оценке."""

    def __init__(self, api_key: str, model: str, timeout: int) -> None:
        """
        Инициализация LLM клиента.

        Args:
            api_key: API ключ для OpenRouter
            model: Название модели для использования
            timeout: Таймаут запроса в секундах
        """
        self.client = AsyncOpenAI(
            base_url="https://openrouter.ai/api/v1", api_key=api_key, timeout=timeout
        )
        self.model = model
        self.timeout = timeout

        logger.info(f"LLMClient initialized with model: {model}")

    async def get_response(self, user_message: str, history: list[dict[str, str]] = None) -> str:
        """
        Получить ответ от LLM с учетом истории диалога.

        Args:
            user_message: Сообщение от пользователя
            history: История диалога в формате [{"role": "user", "content": "..."}, ...]

        Returns:
            Ответ от LLM

        Raises:
            Exception: При ошибках API или таймауте
        """
        logger.info(f"Sending request to LLM (model: {self.model})")
        logger.debug(f"User message: {user_message}")

        start_time = time.time()

        try:
            # Формируем запрос с системным промптом
            messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]

            # Добавляем историю диалога, если есть
            if history:
                messages.extend(history)
                logger.debug(f"Added {len(history)} messages from history")

            # Добавляем текущее сообщение пользователя
            messages.append({"role": "user", "content": user_message})

            logger.debug(f"Total messages in context: {len(messages)}")

            # Отправляем запрос
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
            )

            # Извлекаем ответ
            assistant_message = response.choices[0].message.content

            # Измеряем время ответа
            elapsed_time = time.time() - start_time

            if elapsed_time > 20:
                logger.warning(f"Slow LLM response: {elapsed_time:.2f}s (threshold: 20s)")

            logger.info(f"Successfully received response from LLM (took {elapsed_time:.2f}s)")
            logger.debug(f"Assistant response: {assistant_message}")

            return assistant_message

        except APITimeoutError as e:
            elapsed_time = time.time() - start_time
            logger.error(f"LLM request timeout after {elapsed_time:.2f}s: {e}", exc_info=True)
            raise TimeoutError("Превышено время ожидания ответа от LLM") from e

        except APIConnectionError as e:
            logger.error(f"Network error connecting to LLM API: {e}", exc_info=True)
            raise ConnectionError("Ошибка сети при подключении к LLM") from e

        except RateLimitError as e:
            logger.error(f"Rate limit exceeded for LLM API: {e}", exc_info=True)
            raise ValueError("Превышен лимит запросов к LLM API") from e

        except APIStatusError as e:
            logger.error(f"LLM API error (status {e.status_code}): {e.message}", exc_info=True)
            raise RuntimeError(f"Ошибка API LLM: {e.message}") from e

        except Exception as e:
            logger.error(f"Unexpected error getting LLM response: {e}", exc_info=True)
            raise RuntimeError(f"Неожиданная ошибка при работе с LLM: {str(e)}") from e
