"""Mock implementation of statistics collector."""

import random
from datetime import datetime, timedelta
from src.api.models import (
    StatsResponse,
    Summary,
    MetricValue,
    ActivityChart,
    RecentConversation,
    TopUser,
)


class MockStatCollector:
    """Mock реализация сборщика статистики с генерацией тестовых данных.
    
    Генерирует реалистичные данные для демонстрации дашборда.
    Использует фиксированный seed для воспроизводимости результатов.
    """

    def __init__(self, seed: int = 42):
        """Инициализация Mock коллектора.
        
        Args:
            seed: Seed для генератора случайных чисел (для воспроизводимости)
        """
        self.seed = seed

    def get_stats(self, period: str) -> StatsResponse:
        """Получить mock статистику за указанный период.
        
        Args:
            period: Период для статистики ("day", "week", "month")
            
        Returns:
            StatsResponse: Сгенерированные тестовые данные
            
        Raises:
            ValueError: Если передан невалидный период
        """
        if period not in ["day", "week", "month"]:
            raise ValueError(f"Invalid period: {period}. Must be 'day', 'week', or 'month'")

        # Устанавливаем seed для воспроизводимости
        random.seed(self.seed + hash(period))

        return StatsResponse(
            period=period,
            summary=self._generate_summary(period),
            activity_chart=self._generate_activity_chart(period),
            recent_conversations=self._generate_recent_conversations(),
            top_users=self._generate_top_users(),
        )

    def _generate_summary(self, period: str) -> Summary:
        """Генерирует сводную статистику."""
        
        # Базовые значения зависят от периода
        period_multipliers = {
            "day": 1.0,
            "week": 7.0,
            "month": 30.0,
        }
        multiplier = period_multipliers[period]

        # Генерируем реалистичные значения
        total_convs = int(random.uniform(100, 200) * multiplier)
        active_users = int(random.uniform(30, 60) * (multiplier ** 0.7))
        avg_length = round(random.uniform(6.0, 12.0), 1)
        growth_rate = round(random.uniform(2.0, 8.0), 1)

        return Summary(
            total_conversations=MetricValue(
                value=total_convs,
                change_percent=round(random.uniform(-5.0, 20.0), 1),
                trend=self._get_trend(random.uniform(-5.0, 20.0)),
                description=self._get_description("conversations", random.uniform(-5.0, 20.0)),
            ),
            active_users=MetricValue(
                value=active_users,
                change_percent=round(random.uniform(-10.0, 15.0), 1),
                trend=self._get_trend(random.uniform(-10.0, 15.0)),
                description=self._get_description("users", random.uniform(-10.0, 15.0)),
            ),
            avg_conversation_length=MetricValue(
                value=avg_length,
                change_percent=round(random.uniform(-3.0, 8.0), 1),
                trend=self._get_trend(random.uniform(-3.0, 8.0)),
                description=self._get_description("length", random.uniform(-3.0, 8.0)),
            ),
            growth_rate=MetricValue(
                value=growth_rate,
                change_percent=round(random.uniform(-2.0, 5.0), 1),
                trend=self._get_trend(random.uniform(-2.0, 5.0)),
                description=self._get_description("growth", random.uniform(-2.0, 5.0)),
            ),
        )

    def _generate_activity_chart(self, period: str) -> ActivityChart:
        """Генерирует данные для графика активности."""
        
        now = datetime.now()
        
        if period == "day":
            # 24 часа по часам
            labels = [(now - timedelta(hours=23-i)).strftime("%H:00") for i in range(24)]
            # Имитируем активность по часам (пики днем и вечером)
            values = [
                round(random.uniform(5, 15) if 0 <= i < 8 else  # Ночь
                      random.uniform(25, 45) if 8 <= i < 18 else  # День
                      random.uniform(35, 55) if 18 <= i < 23 else  # Вечер
                      random.uniform(10, 20), 1)  # Поздний вечер
                for i in range(24)
            ]
        elif period == "week":
            # 7 дней
            labels = [(now - timedelta(days=6-i)).strftime("%Y-%m-%d") for i in range(7)]
            # Имитируем активность по дням (спад в выходные)
            values = [
                round(random.uniform(150, 200) if i < 5 else  # Будни
                      random.uniform(80, 120), 1)  # Выходные
                for i in range(7)
            ]
        else:  # month
            # 30 дней
            labels = [(now - timedelta(days=29-i)).strftime("%Y-%m-%d") for i in range(30)]
            # Имитируем общий тренд роста с флуктуациями
            base_value = 100
            trend = 2  # Рост на 2 единицы в день
            values = [
                round(base_value + i * trend + random.uniform(-20, 30), 1)
                for i in range(30)
            ]

        return ActivityChart(labels=labels, values=values)

    def _generate_recent_conversations(self) -> list[RecentConversation]:
        """Генерирует список последних диалогов."""
        
        conversations = []
        now = datetime.now()
        
        # Генерируем 10 последних диалогов
        for i in range(10):
            conversations.append(
                RecentConversation(
                    conversation_id=f"conv_{random.randint(1000, 9999)}",
                    user_name=self._generate_user_name(),
                    started_at=now - timedelta(
                        hours=random.randint(0, 24),
                        minutes=random.randint(0, 59)
                    ),
                    message_count=random.randint(3, 25),
                    status="active" if random.random() > 0.6 else "completed",
                )
            )
        
        # Сортируем по времени (новые первые)
        conversations.sort(key=lambda x: x.started_at, reverse=True)
        return conversations

    def _generate_top_users(self) -> list[TopUser]:
        """Генерирует топ-5 пользователей."""
        
        users = []
        now = datetime.now()
        
        # Генерируем 5 топовых пользователей
        for i in range(5):
            conv_count = random.randint(15, 50) - i * 5  # Убывающий порядок
            users.append(
                TopUser(
                    username=self._generate_username(),
                    conversation_count=conv_count,
                    message_count=conv_count * random.randint(8, 15),
                    last_active=now - timedelta(
                        hours=random.randint(0, 12),
                        minutes=random.randint(0, 59)
                    ),
                )
            )
        
        return users

    @staticmethod
    def _get_trend(change_percent: float) -> str:
        """Определяет направление тренда на основе процента изменения."""
        if change_percent > 2:
            return "up"
        elif change_percent < -2:
            return "down"
        else:
            return "stable"

    @staticmethod
    def _get_description(metric_type: str, change_percent: float) -> str:
        """Генерирует текстовое описание тренда."""
        
        descriptions = {
            "conversations": {
                "up": ["Trending up this period", "Strong growth in conversations", "Increased user engagement"],
                "down": ["Slightly decreased", "Needs attention", "Lower activity this period"],
                "stable": ["Stable performance", "Consistent activity", "Maintaining current level"],
            },
            "users": {
                "up": ["Growing user base", "More active users", "Strong user retention"],
                "down": ["Some users inactive", "User retention declined", "Acquisition needs attention"],
                "stable": ["Stable user base", "Consistent engagement", "Steady performance"],
            },
            "length": {
                "up": ["Conversations are getting longer", "More detailed discussions", "Increased engagement depth"],
                "down": ["Shorter conversations", "Quick interactions", "Less detailed exchanges"],
                "stable": ["Consistent conversation depth", "Stable interaction length", "Maintaining quality"],
            },
            "growth": {
                "up": ["Steady growth", "Accelerating performance", "Meets growth projections"],
                "down": ["Growth slowing down", "Below target", "Needs optimization"],
                "stable": ["Stable growth rate", "Consistent performance", "On track"],
            },
        }
        
        trend = MockStatCollector._get_trend(change_percent)
        return random.choice(descriptions[metric_type][trend])

    @staticmethod
    def _generate_user_name() -> str:
        """Генерирует случайное имя пользователя."""
        first_names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Wilson", "Moore"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"

    @staticmethod
    def _generate_username() -> str:
        """Генерирует случайный username."""
        prefixes = ["user", "dev", "admin", "test", "demo"]
        return f"{random.choice(prefixes)}_{random.randint(100, 999)}"

