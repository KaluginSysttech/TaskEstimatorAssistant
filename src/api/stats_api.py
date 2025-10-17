"""FastAPI routes for statistics API."""

from fastapi import APIRouter, HTTPException, Depends, Query
from src.api.models import StatsResponse
from src.api.dependencies import get_stat_collector
from src.stats.collector import StatCollector

router = APIRouter(prefix="/api/v1", tags=["statistics"])


@router.get(
    "/stats",
    response_model=StatsResponse,
    summary="Get conversation statistics",
    description="""
    Получить статистику диалогов за указанный период.
    
    Возвращает:
    - Сводные метрики (всего диалогов, активные пользователи, средняя длина, рост)
    - Данные для графика активности
    - Список последних диалогов
    - Топ-5 наиболее активных пользователей
    
    Периоды:
    - **day**: последние 24 часа (данные по часам)
    - **week**: последние 7 дней (данные по дням)
    - **month**: последние 30 дней (данные по дням)
    """,
    responses={
        200: {
            "description": "Successful response with statistics data",
            "content": {
                "application/json": {
                    "example": {
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
                        "recent_conversations": [
                            {
                                "conversation_id": "conv_1234",
                                "user_name": "John Doe",
                                "started_at": "2025-10-17T14:30:00Z",
                                "message_count": 12,
                                "status": "active"
                            }
                        ],
                        "top_users": [
                            {
                                "username": "user_456",
                                "conversation_count": 34,
                                "message_count": 287,
                                "last_active": "2025-10-17T15:45:00Z"
                            }
                        ]
                    }
                }
            }
        },
        400: {
            "description": "Invalid period parameter",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid period: invalid. Must be 'day', 'week', or 'month'"}
                }
            }
        }
    }
)
async def get_stats(
    period: str = Query(
        ...,
        description="Time period for statistics",
        pattern="^(day|week|month)$",
        examples=["day", "week", "month"]
    ),
    collector: StatCollector = Depends(get_stat_collector)
) -> StatsResponse:
    """
    Endpoint для получения статистики диалогов.
    
    Args:
        period: Период для статистики (day, week, month)
        collector: Инжектируемый сборщик статистики
        
    Returns:
        StatsResponse: Полные данные статистики
        
    Raises:
        HTTPException: 400 если передан невалидный период
    """
    try:
        return await collector.get_stats(period)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

