"""Real implementation of statistics collector with database queries."""

from datetime import datetime, timedelta
from sqlalchemy import func, select, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.models import (
    StatsResponse,
    Summary,
    MetricValue,
    ActivityChart,
    RecentConversation,
    TopUser,
)
from src.db.models import User, Message


class RealStatCollector:
    """Реальная реализация сборщика статистики с данными из БД.
    
    Получает статистику диалогов из базы данных PostgreSQL.
    Работает с таблицами users и messages.
    """

    def __init__(self, session: AsyncSession):
        """Инициализация Real коллектора.
        
        Args:
            session: Асинхронная сессия SQLAlchemy для работы с БД
        """
        self.session = session

    async def get_stats(self, period: str) -> StatsResponse:
        """Получить реальную статистику за указанный период.
        
        Args:
            period: Период для статистики ("day", "week", "month")
            
        Returns:
            StatsResponse: Данные статистики из БД
            
        Raises:
            ValueError: Если передан невалидный период
        """
        if period not in ["day", "week", "month"]:
            raise ValueError(f"Invalid period: {period}. Must be 'day', 'week', or 'month'")

        # Определяем временной диапазон
        now = datetime.utcnow()
        if period == "day":
            start_date = now - timedelta(days=1)
            prev_start_date = now - timedelta(days=2)
        elif period == "week":
            start_date = now - timedelta(days=7)
            prev_start_date = now - timedelta(days=14)
        else:  # month
            start_date = now - timedelta(days=30)
            prev_start_date = now - timedelta(days=60)

        # Собираем все данные параллельно
        summary = await self._generate_summary(start_date, prev_start_date)
        activity_chart = await self._generate_activity_chart(period, start_date)
        recent_conversations = await self._generate_recent_conversations()
        top_users = await self._generate_top_users(start_date)

        return StatsResponse(
            period=period,
            summary=summary,
            activity_chart=activity_chart,
            recent_conversations=recent_conversations,
            top_users=top_users,
        )

    async def _generate_summary(self, start_date: datetime, prev_start_date: datetime) -> Summary:
        """Генерирует сводную статистику на основе реальных данных."""
        
        # Количество диалогов (уникальных пользователей с сообщениями)
        current_convs_query = select(func.count(distinct(Message.user_id))).where(
            Message.created_at >= start_date,
            Message.is_deleted == False
        )
        current_convs_result = await self.session.execute(current_convs_query)
        current_convs = current_convs_result.scalar() or 0

        # Количество диалогов за предыдущий период
        prev_convs_query = select(func.count(distinct(Message.user_id))).where(
            Message.created_at >= prev_start_date,
            Message.created_at < start_date,
            Message.is_deleted == False
        )
        prev_convs_result = await self.session.execute(prev_convs_query)
        prev_convs = prev_convs_result.scalar() or 0

        # Активные пользователи (пользователи с сообщениями в периоде)
        current_users_query = select(func.count(distinct(User.id))).select_from(User).join(
            Message, User.id == Message.user_id
        ).where(
            Message.created_at >= start_date,
            Message.is_deleted == False,
            User.is_deleted == False
        )
        current_users_result = await self.session.execute(current_users_query)
        current_users = current_users_result.scalar() or 0

        # Активные пользователи за предыдущий период
        prev_users_query = select(func.count(distinct(User.id))).select_from(User).join(
            Message, User.id == Message.user_id
        ).where(
            Message.created_at >= prev_start_date,
            Message.created_at < start_date,
            Message.is_deleted == False,
            User.is_deleted == False
        )
        prev_users_result = await self.session.execute(prev_users_query)
        prev_users = prev_users_result.scalar() or 0

        # Средняя длина диалога (сообщений на пользователя)
        avg_length_query = select(
            func.count(Message.id) / func.count(distinct(Message.user_id))
        ).where(
            Message.created_at >= start_date,
            Message.is_deleted == False
        )
        avg_length_result = await self.session.execute(avg_length_query)
        current_avg_length = float(avg_length_result.scalar() or 0)

        # Средняя длина за предыдущий период
        prev_avg_length_query = select(
            func.count(Message.id) / func.count(distinct(Message.user_id))
        ).where(
            Message.created_at >= prev_start_date,
            Message.created_at < start_date,
            Message.is_deleted == False
        )
        prev_avg_length_result = await self.session.execute(prev_avg_length_query)
        prev_avg_length = float(prev_avg_length_result.scalar() or 0)

        # Рассчитываем процентные изменения
        convs_change = self._calculate_change_percent(current_convs, prev_convs)
        users_change = self._calculate_change_percent(current_users, prev_users)
        length_change = self._calculate_change_percent(current_avg_length, prev_avg_length)
        
        # Growth rate (процент роста новых пользователей)
        total_users_query = select(func.count(User.id)).where(User.is_deleted == False)
        total_users_result = await self.session.execute(total_users_query)
        total_users = total_users_result.scalar() or 1
        
        growth_rate = (current_users / total_users * 100) if total_users > 0 else 0

        return Summary(
            total_conversations=MetricValue(
                value=current_convs,
                change_percent=round(convs_change, 1),
                trend=self._get_trend(convs_change),
                description=self._get_description("conversations", convs_change),
            ),
            active_users=MetricValue(
                value=current_users,
                change_percent=round(users_change, 1),
                trend=self._get_trend(users_change),
                description=self._get_description("users", users_change),
            ),
            avg_conversation_length=MetricValue(
                value=round(current_avg_length, 1),
                change_percent=round(length_change, 1),
                trend=self._get_trend(length_change),
                description=self._get_description("length", length_change),
            ),
            growth_rate=MetricValue(
                value=round(growth_rate, 1),
                change_percent=round(users_change, 1),
                trend=self._get_trend(users_change),
                description=self._get_description("growth", users_change),
            ),
        )

    async def _generate_activity_chart(self, period: str, start_date: datetime) -> ActivityChart:
        """Генерирует данные для графика активности на основе реальных данных."""
        
        now = datetime.utcnow()
        labels = []
        values = []

        if period == "day":
            # 24 часа по часам
            for i in range(24):
                hour_start = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=23-i)
                hour_end = hour_start + timedelta(hours=1)
                
                query = select(func.count(Message.id)).where(
                    Message.created_at >= hour_start,
                    Message.created_at < hour_end,
                    Message.is_deleted == False
                )
                result = await self.session.execute(query)
                count = result.scalar() or 0
                
                labels.append(hour_start.strftime("%H:00"))
                values.append(count)
        
        elif period == "week":
            # 7 дней
            for i in range(7):
                day_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=6-i)
                day_end = day_start + timedelta(days=1)
                
                query = select(func.count(Message.id)).where(
                    Message.created_at >= day_start,
                    Message.created_at < day_end,
                    Message.is_deleted == False
                )
                result = await self.session.execute(query)
                count = result.scalar() or 0
                
                labels.append(day_start.strftime("%Y-%m-%d"))
                values.append(count)
        
        else:  # month
            # 30 дней
            for i in range(30):
                day_start = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=29-i)
                day_end = day_start + timedelta(days=1)
                
                query = select(func.count(Message.id)).where(
                    Message.created_at >= day_start,
                    Message.created_at < day_end,
                    Message.is_deleted == False
                )
                result = await self.session.execute(query)
                count = result.scalar() or 0
                
                labels.append(day_start.strftime("%Y-%m-%d"))
                values.append(count)

        return ActivityChart(labels=labels, values=values)

    async def _generate_recent_conversations(self) -> list[RecentConversation]:
        """Генерирует список последних диалогов на основе реальных данных."""
        
        # Получаем последние 10 пользователей с их последними сообщениями
        query = (
            select(
                User.id,
                User.username,
                User.telegram_id,
                func.min(Message.created_at).label("started_at"),
                func.count(Message.id).label("message_count"),
                func.max(Message.created_at).label("last_message_at")
            )
            .select_from(User)
            .join(Message, User.id == Message.user_id)
            .where(
                User.is_deleted == False,
                Message.is_deleted == False
            )
            .group_by(User.id, User.username, User.telegram_id)
            .order_by(func.max(Message.created_at).desc())
            .limit(10)
        )
        
        result = await self.session.execute(query)
        rows = result.all()
        
        conversations = []
        now = datetime.utcnow()
        
        for row in rows:
            # Определяем статус (active если последнее сообщение меньше часа назад)
            time_since_last = now - row.last_message_at
            status = "active" if time_since_last.total_seconds() < 3600 else "completed"
            
            conversations.append(
                RecentConversation(
                    conversation_id=f"user_{row.telegram_id}",
                    user_name=row.username or f"User {row.telegram_id}",
                    started_at=row.started_at,
                    message_count=row.message_count,
                    status=status,
                )
            )
        
        return conversations

    async def _generate_top_users(self, start_date: datetime) -> list[TopUser]:
        """Генерирует топ-5 пользователей на основе реальных данных."""
        
        # Получаем топ-5 пользователей по количеству диалогов (сообщений) за период
        query = (
            select(
                User.username,
                User.telegram_id,
                func.count(Message.id).label("message_count"),
                func.max(Message.created_at).label("last_active")
            )
            .select_from(User)
            .join(Message, User.id == Message.user_id)
            .where(
                User.is_deleted == False,
                Message.is_deleted == False,
                Message.created_at >= start_date
            )
            .group_by(User.id, User.username, User.telegram_id)
            .order_by(func.count(Message.id).desc())
            .limit(5)
        )
        
        result = await self.session.execute(query)
        rows = result.all()
        
        users = []
        for row in rows:
            # Для conversation_count используем примерную оценку
            # (каждые 10 сообщений = 1 диалог)
            conversation_count = max(1, row.message_count // 10)
            
            users.append(
                TopUser(
                    username=row.username or f"user_{row.telegram_id}",
                    conversation_count=conversation_count,
                    message_count=row.message_count,
                    last_active=row.last_active,
                )
            )
        
        return users

    @staticmethod
    def _calculate_change_percent(current: float, previous: float) -> float:
        """Рассчитывает процент изменения между текущим и предыдущим значением."""
        if previous == 0:
            return 100.0 if current > 0 else 0.0
        return ((current - previous) / previous) * 100

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
                "up": "Trending up this period",
                "down": "Slightly decreased",
                "stable": "Stable performance",
            },
            "users": {
                "up": "Growing user base",
                "down": "Some users inactive",
                "stable": "Stable user base",
            },
            "length": {
                "up": "Conversations are getting longer",
                "down": "Shorter conversations",
                "stable": "Consistent conversation depth",
            },
            "growth": {
                "up": "Steady growth",
                "down": "Growth slowing down",
                "stable": "Stable growth rate",
            },
        }
        
        trend = RealStatCollector._get_trend(change_percent)
        return descriptions[metric_type][trend]

