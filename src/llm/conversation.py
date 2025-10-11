"""Управление историей диалогов пользователей."""

import logging

logger = logging.getLogger(__name__)


class Conversation:
    """
    In-memory хранение истории диалогов по user_id.

    Хранит историю сообщений для каждого пользователя с ограничением
    по количеству сообщений. При превышении лимита удаляются старые сообщения.
    """

    def __init__(self, max_messages: int = 20) -> None:
        """
        Инициализация хранилища диалогов.

        Args:
            max_messages: Максимальное количество сообщений в истории (default: 20)
        """
        self._conversations: dict[int, list[dict[str, str]]] = {}
        self._max_messages = max_messages

        logger.info(f"Conversation storage initialized with max_messages={max_messages}")

    def add_message(self, user_id: int, role: str, content: str) -> None:
        """
        Добавить сообщение в историю пользователя.

        Args:
            user_id: ID пользователя Telegram
            role: Роль отправителя ("user" или "assistant")
            content: Содержимое сообщения
        """
        if user_id not in self._conversations:
            self._conversations[user_id] = []
            logger.info(f"Created new conversation for user {user_id}")

        # Добавляем сообщение
        message = {"role": role, "content": content}
        self._conversations[user_id].append(message)

        # Ограничиваем историю
        if len(self._conversations[user_id]) > self._max_messages:
            removed = self._conversations[user_id].pop(0)
            logger.warning(
                f"History limit reached for user {user_id}. "
                f"Removed oldest message (role: {removed['role']})"
            )

        current_count = len(self._conversations[user_id])
        logger.debug(
            f"Added message to user {user_id} history "
            f"(role: {role}, total messages: {current_count})"
        )

    def get_history(self, user_id: int) -> list[dict[str, str]]:
        """
        Получить историю диалога пользователя.

        Args:
            user_id: ID пользователя Telegram

        Returns:
            Список сообщений в формате [{"role": "user", "content": "..."}, ...]
            Возвращает пустой список, если истории нет
        """
        history = self._conversations.get(user_id, [])
        logger.debug(f"Retrieved history for user {user_id}: {len(history)} messages")
        return history.copy()  # Возвращаем копию для безопасности

    def clear_history(self, user_id: int) -> None:
        """
        Очистить историю диалога пользователя.

        Args:
            user_id: ID пользователя Telegram
        """
        if user_id in self._conversations:
            message_count = len(self._conversations[user_id])
            del self._conversations[user_id]
            logger.info(f"Cleared history for user {user_id} ({message_count} messages)")
        else:
            logger.debug(f"No history to clear for user {user_id}")

    def get_stats(self) -> dict[str, int]:
        """
        Получить статистику по хранилищу.

        Returns:
            Словарь со статистикой: total_users, total_messages
        """
        total_users = len(self._conversations)
        total_messages = sum(len(msgs) for msgs in self._conversations.values())

        return {"total_users": total_users, "total_messages": total_messages}
