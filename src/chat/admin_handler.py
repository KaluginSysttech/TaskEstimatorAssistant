"""Admin mode handler for statistics queries."""

import logging
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.stats.collector import StatCollector

logger = logging.getLogger(__name__)


class AdminHandler:
    """
    Handler for admin mode statistics queries.

    Provides mock responses based on keywords and integrates with StatCollector
    to fetch real statistics data.
    """

    def __init__(self, stat_collector: "StatCollector") -> None:
        """
        Initialize admin handler.

        Args:
            stat_collector: Statistics collector for fetching data
        """
        self.stat_collector = stat_collector
        logger.info("AdminHandler initialized")

    async def handle_admin_query(
        self,
        message: str,
        history: list[dict[str, str]] | None = None,
    ) -> str:
        """
        Process an admin query about statistics.

        Args:
            message: User query text
            history: Conversation history (currently unused)

        Returns:
            Response text with statistics information
        """
        logger.info(f"Processing admin query: {message}")

        message_lower = message.lower()

        try:
            # Detect query type based on keywords
            if any(
                keyword in message_lower
                for keyword in ["диалог", "conversation", "всего", "total", "количество"]
            ):
                return await self._handle_conversations_query(message_lower)

            elif any(
                keyword in message_lower
                for keyword in ["пользовател", "user", "активн", "active"]
            ):
                return await self._handle_users_query(message_lower)

            elif any(
                keyword in message_lower
                for keyword in ["статистик", "statistic", "метрик", "metric", "данн", "data"]
            ):
                return await self._handle_general_stats_query(message_lower)

            elif any(
                keyword in message_lower
                for keyword in ["график", "chart", "активность", "activity", "динамик"]
            ):
                return await self._handle_activity_query(message_lower)

            else:
                # Default response for unclear queries
                return self._get_help_response()

        except Exception as e:
            logger.error(f"Error processing admin query: {e}", exc_info=True)
            return (
                "Произошла ошибка при получении статистики. "
                "Пожалуйста, попробуйте переформулировать запрос."
            )

    async def _handle_conversations_query(self, message_lower: str) -> str:
        """Handle queries about conversations count."""
        # Determine period
        period = self._detect_period(message_lower)

        # Get stats
        stats = await self.stat_collector.get_stats(period)
        total = int(stats.summary.total_conversations.value)
        change = stats.summary.total_conversations.change_percent
        trend = stats.summary.total_conversations.trend

        trend_text = "увеличение" if trend == "up" else "уменьшение" if trend == "down" else "стабильность"

        response = (
            f"📊 **Статистика диалогов за {self._format_period(period)}:**\n\n"
            f"Всего диалогов: **{total}**\n"
            f"Изменение: **{change:+.1f}%** ({trend_text})\n\n"
            f"```sql\n"
            f"-- Пример SQL запроса для получения этих данных:\n"
            f"SELECT COUNT(DISTINCT user_id) as total_conversations\n"
            f"FROM messages\n"
            f"WHERE created_at >= datetime('now', '-{self._get_period_days(period)} days')\n"
            f"  AND is_deleted = 0;\n"
            f"```"
        )

        return response

    async def _handle_users_query(self, message_lower: str) -> str:
        """Handle queries about active users."""
        period = self._detect_period(message_lower)

        stats = await self.stat_collector.get_stats(period)
        users = int(stats.summary.active_users.value)
        change = stats.summary.active_users.change_percent

        response = (
            f"👥 **Активные пользователи за {self._format_period(period)}:**\n\n"
            f"Количество: **{users}**\n"
            f"Изменение: **{change:+.1f}%**\n\n"
            f"**Топ-5 пользователей:**\n"
        )

        for i, user in enumerate(stats.top_users[:5], 1):
            response += (
                f"{i}. @{user.username} - "
                f"{user.conversation_count} диалогов, "
                f"{user.message_count} сообщений\n"
            )

        response += (
            f"\n```sql\n"
            f"-- Пример SQL запроса:\n"
            f"SELECT COUNT(DISTINCT telegram_id) as active_users\n"
            f"FROM users u\n"
            f"JOIN messages m ON u.id = m.user_id\n"
            f"WHERE m.created_at >= datetime('now', '-{self._get_period_days(period)} days')\n"
            f"  AND m.is_deleted = 0;\n"
            f"```"
        )

        return response

    async def _handle_general_stats_query(self, message_lower: str) -> str:
        """Handle general statistics queries."""
        period = self._detect_period(message_lower)

        stats = await self.stat_collector.get_stats(period)

        response = (
            f"📈 **Общая статистика за {self._format_period(period)}:**\n\n"
            f"📊 **Диалоги:** {int(stats.summary.total_conversations.value)} "
            f"({stats.summary.total_conversations.change_percent:+.1f}%)\n"
            f"👥 **Пользователи:** {int(stats.summary.active_users.value)} "
            f"({stats.summary.active_users.change_percent:+.1f}%)\n"
            f"💬 **Средняя длина диалога:** {stats.summary.avg_conversation_length.value:.1f} сообщений "
            f"({stats.summary.avg_conversation_length.change_percent:+.1f}%)\n"
            f"📈 **Скорость роста:** {stats.summary.growth_rate.value:.1f}% "
            f"({stats.summary.growth_rate.change_percent:+.1f}%)\n\n"
            f"Данные получены из базы данных в реальном времени."
        )

        return response

    async def _handle_activity_query(self, message_lower: str) -> str:
        """Handle queries about activity trends."""
        period = self._detect_period(message_lower)

        stats = await self.stat_collector.get_stats(period)

        # Get last few data points
        labels = stats.activity_chart.labels[-5:]
        values = stats.activity_chart.values[-5:]

        response = (
            f"📊 **Динамика активности за {self._format_period(period)}:**\n\n"
            f"Последние данные:\n"
        )

        for label, value in zip(labels, values):
            response += f"• {label}: {int(value)} сообщений\n"

        avg_activity = sum(values) / len(values) if values else 0
        response += f"\nСредняя активность: **{avg_activity:.1f}** сообщений\n"

        return response

    def _get_help_response(self) -> str:
        """Get help response for unclear queries."""
        return (
            "🤖 **Режим администратора**\n\n"
            "Я могу ответить на вопросы о статистике диалогов:\n\n"
            "• Количество диалогов (за день/неделю/месяц)\n"
            "• Активные пользователи\n"
            "• Общая статистика\n"
            "• Динамика активности\n\n"
            "**Примеры запросов:**\n"
            "• \"Сколько диалогов было на этой неделе?\"\n"
            "• \"Покажи активных пользователей\"\n"
            "• \"Общая статистика за месяц\"\n"
            "• \"Динамика активности за неделю\""
        )

    def _detect_period(self, message: str) -> str:
        """
        Detect time period from message.

        Args:
            message: Message text (lowercase)

        Returns:
            Period string: "day", "week", or "month"
        """
        if any(keyword in message for keyword in ["день", "сегодня", "day", "today", "24"]):
            return "day"
        elif any(keyword in message for keyword in ["месяц", "month", "30"]):
            return "month"
        else:
            # Default to week
            return "week"

    def _format_period(self, period: str) -> str:
        """Format period for display."""
        period_map = {
            "day": "последние 24 часа",
            "week": "последнюю неделю",
            "month": "последний месяц",
        }
        return period_map.get(period, "неделю")

    def _get_period_days(self, period: str) -> int:
        """Get number of days for period."""
        period_days = {
            "day": 1,
            "week": 7,
            "month": 30,
        }
        return period_days.get(period, 7)

