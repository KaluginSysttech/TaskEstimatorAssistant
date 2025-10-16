"""Repository для работы с сообщениями и пользователями."""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Message, User

logger = logging.getLogger(__name__)


class MessageRepository:
    """
    Repository для работы с сообщениями в базе данных.

    Предоставляет простой интерфейс для операций с историей диалогов.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация repository.

        Args:
            session: Асинхронная сессия SQLAlchemy
        """
        self.session = session

    async def get_or_create_user(self, telegram_id: int, username: str | None) -> User:
        """
        Получить существующего пользователя или создать нового.

        Args:
            telegram_id: ID пользователя в Telegram
            username: Имя пользователя в Telegram (может быть None)

        Returns:
            User: Объект пользователя
        """
        # Ищем пользователя
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id, User.is_deleted == False)
        )
        user = result.scalar_one_or_none()

        if user is None:
            # Создаём нового пользователя
            user = User(telegram_id=telegram_id, username=username, is_deleted=False)
            self.session.add(user)
            await self.session.flush()  # Чтобы получить ID
            logger.info(f"Created new user: telegram_id={telegram_id}, username={username}")
        else:
            # Обновляем username, если изменился
            if user.username != username:
                user.username = username
                logger.info(
                    f"Updated username for user {telegram_id}: {user.username} -> {username}"
                )

        return user

    async def add_message(
        self, telegram_id: int, role: str, content: str, username: str | None = None
    ) -> Message:
        """
        Добавить сообщение в историю пользователя.

        Args:
            telegram_id: ID пользователя в Telegram
            role: Роль отправителя ("user" или "assistant")
            content: Содержимое сообщения
            username: Имя пользователя (опционально, для get_or_create_user)

        Returns:
            Message: Созданное сообщение
        """
        # Получаем или создаём пользователя
        user = await self.get_or_create_user(telegram_id, username)

        # Создаём сообщение с автоматическим вычислением длины
        message = Message(
            user_id=user.id,
            role=role,
            content=content,
            content_length=len(content),
            is_deleted=False,
        )

        self.session.add(message)
        await self.session.flush()

        logger.debug(
            f"Added message for user {telegram_id}: role={role}, length={len(content)}"
        )

        return message

    async def get_history(
        self, telegram_id: int, limit: int | None = None
    ) -> list[dict[str, str]]:
        """
        Получить историю сообщений пользователя.

        Args:
            telegram_id: ID пользователя в Telegram
            limit: Максимальное количество сообщений (None = все)

        Returns:
            Список сообщений в формате [{"role": "user", "content": "..."}, ...]
            Возвращает пустой список, если пользователя или сообщений нет
        """
        # Сначала находим пользователя
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id, User.is_deleted == False)
        )
        user = result.scalar_one_or_none()

        if user is None:
            logger.debug(f"No user found with telegram_id={telegram_id}")
            return []

        # Получаем сообщения пользователя (только не удалённые)
        query = (
            select(Message)
            .where(Message.user_id == user.id, Message.is_deleted == False)
            .order_by(Message.created_at.asc())
        )

        if limit is not None:
            # Берём последние N сообщений
            # Для этого сортируем по убыванию, берём limit, и переворачиваем
            query = (
                select(Message)
                .where(Message.user_id == user.id, Message.is_deleted == False)
                .order_by(Message.created_at.desc())
                .limit(limit)
            )
            result = await self.session.execute(query)
            messages = list(reversed(result.scalars().all()))
        else:
            result = await self.session.execute(query)
            messages = result.scalars().all()

        # Преобразуем в формат для LLM
        history = [{"role": msg.role, "content": msg.content} for msg in messages]

        logger.debug(
            f"Retrieved history for user {telegram_id}: {len(history)} messages"
        )

        return history

    async def clear_history(self, telegram_id: int) -> int:
        """
        Очистить историю диалога пользователя (soft delete).

        Args:
            telegram_id: ID пользователя в Telegram

        Returns:
            Количество помеченных как удалённые сообщений
        """
        # Находим пользователя
        result = await self.session.execute(
            select(User).where(User.telegram_id == telegram_id, User.is_deleted == False)
        )
        user = result.scalar_one_or_none()

        if user is None:
            logger.debug(f"No user found with telegram_id={telegram_id}")
            return 0

        # Получаем все не удалённые сообщения
        result = await self.session.execute(
            select(Message).where(
                Message.user_id == user.id, Message.is_deleted == False
            )
        )
        messages = result.scalars().all()

        # Помечаем как удалённые
        count = 0
        for message in messages:
            message.is_deleted = True
            count += 1

        await self.session.flush()

        logger.info(f"Cleared history for user {telegram_id}: {count} messages marked as deleted")

        return count

