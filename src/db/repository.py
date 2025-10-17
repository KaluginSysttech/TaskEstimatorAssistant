"""Repository для работы с сообщениями и пользователями."""

import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import ChatMessage, ChatSession, Message, User

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


class ChatRepository:
    """
    Repository для работы с чат-сессиями и сообщениями веб-интерфейса.

    Предоставляет интерфейс для операций с историей чата в веб-приложении.
    """

    def __init__(self, session: AsyncSession) -> None:
        """
        Инициализация repository.

        Args:
            session: Асинхронная сессия SQLAlchemy
        """
        self.session = session

    async def get_or_create_session(self, session_id: str) -> ChatSession:
        """
        Получить существующую сессию или создать новую.

        Args:
            session_id: UUID сессии от клиента

        Returns:
            ChatSession: Объект сессии чата
        """
        # Ищем сессию
        result = await self.session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        chat_session = result.scalar_one_or_none()

        if chat_session is None:
            # Создаём новую сессию
            chat_session = ChatSession(session_id=session_id)
            self.session.add(chat_session)
            await self.session.flush()  # Чтобы получить ID
            logger.info(f"Created new chat session: session_id={session_id}")
        else:
            # Обновляем last_active
            from datetime import datetime
            chat_session.last_active = datetime.utcnow()
            logger.debug(f"Updated last_active for session: session_id={session_id}")

        return chat_session

    async def add_chat_message(
        self, session_id: str, role: str, content: str, mode: str = "normal"
    ) -> ChatMessage:
        """
        Добавить сообщение в историю чата.

        Args:
            session_id: UUID сессии от клиента
            role: Роль отправителя ("user" или "assistant")
            content: Содержимое сообщения
            mode: Режим чата ("normal" или "admin")

        Returns:
            ChatMessage: Созданное сообщение
        """
        # Получаем или создаём сессию
        chat_session = await self.get_or_create_session(session_id)

        # Создаём сообщение
        message = ChatMessage(
            session_id=chat_session.id,
            role=role,
            content=content,
            mode=mode,
        )

        self.session.add(message)
        await self.session.flush()

        logger.debug(
            f"Added chat message for session {session_id}: role={role}, mode={mode}, length={len(content)}"
        )

        return message

    async def get_chat_history(
        self, session_id: str, limit: int | None = None
    ) -> list[dict[str, str]]:
        """
        Получить историю сообщений чата.

        Args:
            session_id: UUID сессии от клиента
            limit: Максимальное количество сообщений (None = все)

        Returns:
            Список сообщений в формате [{"role": "user", "content": "..."}, ...]
            Возвращает пустой список, если сессии или сообщений нет
        """
        # Находим сессию
        result = await self.session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        chat_session = result.scalar_one_or_none()

        if chat_session is None:
            logger.debug(f"No chat session found with session_id={session_id}")
            return []

        # Получаем сообщения сессии
        query = (
            select(ChatMessage)
            .where(ChatMessage.session_id == chat_session.id)
            .order_by(ChatMessage.created_at.asc())
        )

        if limit is not None:
            # Берём последние N сообщений
            query = (
                select(ChatMessage)
                .where(ChatMessage.session_id == chat_session.id)
                .order_by(ChatMessage.created_at.desc())
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
            f"Retrieved chat history for session {session_id}: {len(history)} messages"
        )

        return history

    async def clear_chat_history(self, session_id: str) -> int:
        """
        Очистить историю чата (полное удаление).

        Args:
            session_id: UUID сессии от клиента

        Returns:
            Количество удалённых сообщений
        """
        # Находим сессию
        result = await self.session.execute(
            select(ChatSession).where(ChatSession.session_id == session_id)
        )
        chat_session = result.scalar_one_or_none()

        if chat_session is None:
            logger.debug(f"No chat session found with session_id={session_id}")
            return 0

        # Получаем все сообщения
        result = await self.session.execute(
            select(ChatMessage).where(ChatMessage.session_id == chat_session.id)
        )
        messages = result.scalars().all()

        # Удаляем все сообщения
        count = 0
        for message in messages:
            await self.session.delete(message)
            count += 1

        await self.session.flush()

        logger.info(f"Cleared chat history for session {session_id}: {count} messages deleted")

        return count

