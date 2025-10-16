"""Настройка подключения к базе данных."""

import logging
from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.db.models import Base

logger = logging.getLogger(__name__)

# Global engine и session factory (будут инициализированы в init_db)
engine = None
AsyncSessionLocal = None


def init_db(database_url: str) -> None:
    """
    Инициализация подключения к базе данных.

    Args:
        database_url: URL подключения к PostgreSQL
    """
    global engine, AsyncSessionLocal

    logger.info(f"Initializing database connection: {database_url.split('@')[0]}@***")

    engine = create_async_engine(
        database_url,
        echo=False,  # Не логировать SQL запросы (можно включить для отладки)
        pool_pre_ping=True,  # Проверка соединения перед использованием
        pool_size=5,  # Размер пула соединений
        max_overflow=10,  # Максимальное количество дополнительных соединений
    )

    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,  # Не истекать объекты после commit
        autoflush=False,  # Не автоматически flush перед запросами
        autocommit=False,  # Не автоматически commit
    )

    logger.info("Database connection initialized successfully")


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Получить сессию для работы с базой данных.

    Yields:
        AsyncSession: Асинхронная сессия SQLAlchemy

    Raises:
        RuntimeError: Если база данных не инициализирована
    """
    if AsyncSessionLocal is None:
        raise RuntimeError(
            "Database not initialized. Call init_db() first with database_url."
        )

    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """
    Создать все таблицы в базе данных.

    Используется для тестирования. В продакшене используйте Alembic миграции.
    """
    if engine is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created successfully")

