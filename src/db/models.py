"""SQLAlchemy модели для базы данных."""

from datetime import datetime

from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Базовый класс для всех моделей."""

    pass


class User(Base):
    """
    Модель пользователя Telegram.

    Хранит информацию о пользователях бота с поддержкой soft delete.
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(
        BigInteger, unique=True, index=True, nullable=False
    )
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # Relationship
    messages: Mapped[list["Message"]] = relationship(
        "Message", back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Строковое представление пользователя."""
        return f"<User(id={self.id}, telegram_id={self.telegram_id}, username={self.username})>"


class Message(Base):
    """
    Модель сообщения в диалоге.

    Хранит историю сообщений пользователей и ассистента с метаданными.
    """

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    content_length: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False, index=True
    )
    is_deleted: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False, index=True
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="messages")

    def __repr__(self) -> str:
        """Строковое представление сообщения."""
        return (
            f"<Message(id={self.id}, user_id={self.user_id}, "
            f"role={self.role}, length={self.content_length})>"
        )

