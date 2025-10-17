"""Pydantic models for statistics API."""

from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal


class MetricValue(BaseModel):
    """Модель для значения метрики с трендом."""

    value: float = Field(..., description="Значение метрики")
    change_percent: float = Field(..., description="Процент изменения относительно предыдущего периода")
    trend: Literal["up", "down", "stable"] = Field(..., description="Направление тренда")
    description: str = Field(..., description="Текстовое описание тренда")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "value": 145,
                    "change_percent": 12.5,
                    "trend": "up",
                    "description": "Trending up this period"
                }
            ]
        }
    }


class Summary(BaseModel):
    """Сводная статистика по основным метрикам."""

    total_conversations: MetricValue = Field(..., description="Всего диалогов за период")
    active_users: MetricValue = Field(..., description="Количество активных пользователей")
    avg_conversation_length: MetricValue = Field(..., description="Средняя длина диалога (сообщений)")
    growth_rate: MetricValue = Field(..., description="Скорость роста активности (%)")


class ActivityChart(BaseModel):
    """Данные для графика активности."""

    labels: list[str] = Field(..., description="Временные метки (даты или часы)")
    values: list[float] = Field(..., description="Значения активности (количество сообщений/диалогов)")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "labels": ["2025-10-11", "2025-10-12", "2025-10-13", "2025-10-14"],
                    "values": [23, 45, 67, 34]
                }
            ]
        }
    }


class RecentConversation(BaseModel):
    """Информация о недавнем диалоге."""

    conversation_id: str = Field(..., description="Уникальный идентификатор диалога")
    user_name: str = Field(..., description="Имя пользователя")
    started_at: datetime = Field(..., description="Время начала диалога")
    message_count: int = Field(..., description="Количество сообщений в диалоге")
    status: Literal["active", "completed"] = Field(..., description="Статус диалога")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "conversation_id": "conv_123",
                    "user_name": "John Doe",
                    "started_at": "2025-10-17T14:30:00Z",
                    "message_count": 12,
                    "status": "active"
                }
            ]
        }
    }


class TopUser(BaseModel):
    """Информация о топовом пользователе."""

    username: str = Field(..., description="Username пользователя")
    conversation_count: int = Field(..., description="Количество диалогов")
    message_count: int = Field(..., description="Количество сообщений")
    last_active: datetime = Field(..., description="Дата последней активности")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "username": "user_456",
                    "conversation_count": 34,
                    "message_count": 287,
                    "last_active": "2025-10-17T15:45:00Z"
                }
            ]
        }
    }


class StatsResponse(BaseModel):
    """Полный ответ со статистикой."""

    period: Literal["day", "week", "month"] = Field(..., description="Запрошенный период")
    summary: Summary = Field(..., description="Сводная статистика")
    activity_chart: ActivityChart = Field(..., description="Данные для графика активности")
    recent_conversations: list[RecentConversation] = Field(
        ...,
        max_length=10,
        description="Список последних диалогов (максимум 10)"
    )
    top_users: list[TopUser] = Field(
        ...,
        max_length=5,
        description="Топ-5 наиболее активных пользователей"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "period": "week",
                    "summary": {
                        "total_conversations": {
                            "value": 145,
                            "change_percent": 12.5,
                            "trend": "up",
                            "description": "Trending up this period"
                        },
                        "active_users": {
                            "value": 42,
                            "change_percent": -5.2,
                            "trend": "down",
                            "description": "Slightly decreased"
                        },
                        "avg_conversation_length": {
                            "value": 8.3,
                            "change_percent": 3.1,
                            "trend": "up",
                            "description": "Conversations are getting longer"
                        },
                        "growth_rate": {
                            "value": 4.5,
                            "change_percent": 0.8,
                            "trend": "up",
                            "description": "Steady growth"
                        }
                    },
                    "activity_chart": {
                        "labels": ["2025-10-11", "2025-10-12", "2025-10-13"],
                        "values": [23, 45, 67]
                    },
                    "recent_conversations": [],
                    "top_users": []
                }
            ]
        }
    }

