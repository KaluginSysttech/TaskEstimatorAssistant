"""Dependency injection for FastAPI."""

from functools import lru_cache

from src.chat.admin_handler import AdminHandler
from src.chat.chat_handler import ChatHandler
from src.config.settings import Settings
from src.db import get_session
from src.db.repository import ChatRepository
from src.llm.llm_client import LLMClient
from src.stats.collector import StatCollector
from src.stats.real_collector import RealStatCollector


async def get_stat_collector():
    """Возвращает экземпляр StatCollector с подключением к БД.
    
    Использует RealStatCollector для получения реальных данных из БД.
    
    Yields:
        StatCollector: Экземпляр сборщика статистики
    """
    async for session in get_session():
        yield RealStatCollector(session)


@lru_cache()
def get_settings() -> Settings:
    """
    Get application settings (cached).
    
    Returns:
        Settings: Application configuration
    """
    return Settings()


@lru_cache()
def get_llm_client() -> LLMClient:
    """
    Get LLM client instance (cached).
    
    Returns:
        LLMClient: Configured LLM client
    """
    settings = get_settings()
    return LLMClient(
        api_key=settings.openrouter_api_key,
        model=settings.openrouter_model,
        timeout=settings.llm_timeout,
        system_prompt_path="prompts/system_prompt.txt",
    )


async def get_chat_handler():
    """
    Get chat handler instance with dependencies.
    
    Yields:
        ChatHandler: Configured chat message handler
    """
    llm_client = get_llm_client()
    
    async for stat_collector in get_stat_collector():
        admin_handler = AdminHandler(stat_collector=stat_collector)
        
        yield ChatHandler(
            llm_client=llm_client,
            admin_handler=admin_handler,
            max_history_messages=20,
        )


async def get_chat_repository():
    """
    Get chat repository with database session.
    
    Yields:
        ChatRepository: Repository for chat operations
    """
    async for session in get_session():
        yield ChatRepository(session)

