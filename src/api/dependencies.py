"""Dependency injection for FastAPI."""

from src.stats.mock_collector import MockStatCollector
from src.stats.collector import StatCollector


def get_stat_collector() -> StatCollector:
    """Возвращает экземпляр StatCollector.
    
    В текущей версии возвращает MockStatCollector.
    В будущем (Sprint F5) будет возвращать RealStatCollector.
    
    Returns:
        StatCollector: Экземпляр сборщика статистики
    """
    return MockStatCollector(seed=42)

