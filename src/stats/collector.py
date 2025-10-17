"""Interface for statistics collectors."""

from typing import Protocol
from src.api.models import StatsResponse


class StatCollector(Protocol):
    """Protocol для сборщиков статистики.
    
    Определяет интерфейс для получения статистики диалогов.
    Может иметь различные реализации:
    - MockStatCollector: генерирует тестовые данные
    - RealStatCollector: получает данные из БД
    """

    def get_stats(self, period: str) -> StatsResponse:
        """Получить статистику за указанный период.
        
        Args:
            period: Период для статистики ("day", "week", "month")
            
        Returns:
            StatsResponse: Полные данные статистики включая:
                - summary: сводные метрики
                - activity_chart: данные для графика
                - recent_conversations: последние диалоги
                - top_users: топ пользователей
                
        Raises:
            ValueError: Если передан невалидный период
        """
        ...

