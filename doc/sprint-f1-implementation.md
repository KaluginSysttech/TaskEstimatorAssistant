# Sprint F1: Требования к дашборду и Mock API - План реализации

## Метаданные спринта

| Параметр | Значение |
|----------|----------|
| Код спринта | F1 |
| Название | Требования к дашборду и Mock API |
| Статус | 🚧 In Progress |
| Дата начала | 2025-10-17 |
| Дата завершения | - |

## Цели спринта

1. Сформировать функциональные требования к дашборду статистики
2. Спроектировать контракт API для фронтенда
3. Реализовать Mock API с тестовыми данными
4. Обеспечить возможность независимой разработки фронтенда

## Функциональные требования к дашборду

### Общие принципы
- Минималистичный интерфейс с фокусом на ключевые метрики
- Адаптация референса дашборда под специфику проекта TEA (статистика диалогов Telegram-бота)
- Реализация на основе существующих данных БД без доработок схемы

### Компоненты дашборда

#### 1. Карточки ключевых метрик (KPI Cards)

**1.1. Всего диалогов (Total Conversations)**
- Общее количество диалогов за выбранный период
- Процент изменения относительно предыдущего периода
- Краткое описание тренда

**1.2. Активные пользователи (Active Users)**
- Количество уникальных пользователей за период
- Процент изменения относительно предыдущего периода
- Краткое описание тренда

**1.3. Средняя длина диалога (Avg. Conversation Length)**
- Среднее количество сообщений в диалоге
- Процент изменения относительно предыдущего периода
- Краткое описание тренда

**1.4. Скорость роста (Growth Rate)**
- Процент роста активности
- Процент изменения относительно предыдущего периода
- Краткое описание тренда

#### 2. График активности (Activity Chart)

**Основные характеристики:**
- Временная серия активности диалогов
- Поддержка трех периодов: day (24 часа), week (7 дней), month (30 дней)
- Отображение количества сообщений/диалогов по часам/дням
- Переключатель периодов

**Данные для отображения:**
- Временные метки (labels)
- Значения активности (values)

#### 3. Список последних диалогов (Recent Conversations)

**Отображаемая информация:**
- ID диалога
- Имя пользователя
- Дата начала
- Количество сообщений
- Статус (active/completed)

**Ограничения:**
- Максимум 10 последних диалогов

#### 4. Топ пользователей (Top Users)

**Отображаемая информация:**
- Username пользователя
- Количество диалогов
- Количество сообщений
- Дата последней активности

**Ограничения:**
- Топ-5 наиболее активных пользователей

## API Контракт

### Endpoint спецификация

**URL:** `GET /api/v1/stats`

**Query параметры:**
- `period` (required): string, enum("day", "week", "month")
  - `day` - данные за последние 24 часа
  - `week` - данные за последние 7 дней
  - `month` - данные за последние 30 дней

**Response:** `200 OK`

Content-Type: `application/json`

### Структура ответа

```json
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
    "labels": ["2025-10-11", "2025-10-12", "...", "2025-10-17"],
    "values": [23, 45, 67, 34, 56, 78, 42]
  },
  "recent_conversations": [
    {
      "conversation_id": "conv_123",
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
```

### Коды ответов

- `200 OK` - успешный запрос
- `400 Bad Request` - невалидный параметр period
- `500 Internal Server Error` - ошибка сервера

## Архитектура реализации

### Структура модулей

```
src/
├── api/
│   ├── __init__.py
│   ├── stats_api.py         # FastAPI приложение и роуты
│   ├── models.py            # Pydantic модели (dataclasses)
│   └── dependencies.py      # Dependency injection
├── stats/
│   ├── __init__.py
│   ├── collector.py         # Интерфейс StatCollector
│   ├── mock_collector.py    # MockStatCollector реализация
│   └── real_collector.py    # RealStatCollector (для F5)
└── api_main.py              # Entrypoint для запуска API
```

### Интерфейс StatCollector

```python
from abc import ABC, abstractmethod
from typing import Protocol
from src.api.models import StatsResponse

class StatCollector(Protocol):
    """Protocol для сборщиков статистики."""
    
    def get_stats(self, period: str) -> StatsResponse:
        """
        Получить статистику за указанный период.
        
        Args:
            period: Период для статистики ("day", "week", "month")
            
        Returns:
            StatsResponse: Данные статистики
        """
        ...
```

### MockStatCollector

**Характеристики:**
- Генерирует реалистичные тестовые данные
- Разные данные для разных периодов
- Использует random с фиксированным seed для воспроизводимости
- Симулирует различные тренды и паттерны активности

**Генерируемые паттерны:**
- Дневная активность: пики в рабочие часы
- Недельная активность: спад в выходные
- Месячная активность: общий тренд роста

### Pydantic модели

```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class MetricValue(BaseModel):
    value: float = Field(..., description="Значение метрики")
    change_percent: float = Field(..., description="Процент изменения")
    trend: Literal["up", "down", "stable"] = Field(..., description="Направление тренда")
    description: str = Field(..., description="Описание тренда")

class Summary(BaseModel):
    total_conversations: MetricValue
    active_users: MetricValue
    avg_conversation_length: MetricValue
    growth_rate: MetricValue

class ActivityChart(BaseModel):
    labels: list[str] = Field(..., description="Метки времени")
    values: list[float] = Field(..., description="Значения активности")

class RecentConversation(BaseModel):
    conversation_id: str
    user_name: str
    started_at: datetime
    message_count: int
    status: Literal["active", "completed"]

class TopUser(BaseModel):
    username: str
    conversation_count: int
    message_count: int
    last_active: datetime

class StatsResponse(BaseModel):
    period: Literal["day", "week", "month"]
    summary: Summary
    activity_chart: ActivityChart
    recent_conversations: list[RecentConversation]
    top_users: list[TopUser]
```

## Технические детали

### Технологический стек

- **FastAPI** - веб-фреймворк для API
- **Pydantic** - валидация данных и сериализация
- **uvicorn** - ASGI сервер
- **python-dateutil** - работа с датами

### Документация API

**Автоматическая генерация:**
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`
- OpenAPI JSON: `http://localhost:8001/openapi.json`

**Метаданные API:**
- Название: TEA Statistics API
- Версия: 1.0.0
- Описание: Mock API для дашборда статистики диалогов

### Конфигурация

**Настройки Mock API:**
- Порт: 8001 (отдельно от основного приложения)
- Host: 0.0.0.0
- Reload: true (для разработки)

**Параметры генерации данных:**
- Количество недавних диалогов: 10
- Количество топ пользователей: 5
- Seed для random: 42 (воспроизводимость)

## Команды запуска

### Makefile команды

```makefile
# Запуск Mock API
run-stats-api:
	uv run uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload

# Тестирование API
test-stats-api:
	@echo "Testing stats API endpoints..."
	@curl -s "http://localhost:8001/api/v1/stats?period=day" | python -m json.tool
	@echo "\n---\n"
	@curl -s "http://localhost:8001/api/v1/stats?period=week" | python -m json.tool
	@echo "\n---\n"
	@curl -s "http://localhost:8001/api/v1/stats?period=month" | python -m json.tool

# Открыть документацию API
open-stats-docs:
	@echo "Opening API documentation..."
	@start http://localhost:8001/docs
```

### Использование

```bash
# 1. Запустить Mock API
make run-stats-api

# 2. В другом терминале протестировать
make test-stats-api

# 3. Открыть Swagger UI
make open-stats-docs
```

## Критерии готовности (Definition of Done)

- [ ] Создан документ с функциональными требованиями
- [ ] Спроектирован и документирован API контракт
- [ ] Реализован интерфейс StatCollector
- [ ] Реализован MockStatCollector с реалистичными данными
- [ ] Создан entrypoint `src/api_main.py`
- [ ] Реализован endpoint GET /api/v1/stats
- [ ] Настроена автоматическая генерация OpenAPI документации
- [ ] Добавлены команды в Makefile
- [ ] API успешно запускается и отвечает на запросы
- [ ] Swagger UI доступен и корректно работает
- [ ] Обновлен frontend-roadmap.md со ссылкой на план

## Зависимости

### Текущие зависимости проекта
```toml
[project]
dependencies = [
    "python-telegram-bot>=21.10",
    "openai>=1.59.8",
    "python-dotenv>=1.0.1",
    "sqlalchemy>=2.0.36",
    "psycopg2-binary>=2.9.10",
    "alembic>=1.14.0",
]
```

### Новые зависимости для Sprint F1
```toml
# Добавить в pyproject.toml
dependencies = [
    # ... существующие
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "python-dateutil>=2.9.0",
]
```

## Риски и ограничения

### Риски
1. **Несоответствие Mock данных реальным** - Mock может генерировать данные, которые отличаются от реальной структуры БД
   - Митигация: Детальный анализ схемы БД перед реализацией MockStatCollector

2. **Изменение требований к UI** - Референс может быть изменен в процессе разработки
   - Митигация: Гибкая структура API контракта, легко расширяемая

### Ограничения
1. Mock API не подключается к реальной БД
2. Данные генерируются случайно, не сохраняются между запусками
3. Нет аутентификации/авторизации (будет добавлено позже)

## Связь с другими спринтами

- **Sprint F2** (Каркас frontend): Использует API контракт из F1
- **Sprint F3** (Dashboard): Интегрируется с Mock API из F1
- **Sprint F5** (Real API): Заменяет MockStatCollector на RealStatCollector

## Примечания

- Mock API должен максимально точно имитировать поведение будущего реального API
- Все тренды и проценты изменений генерируются динамически
- Данные должны выглядеть реалистично для демонстрации фронтенда
- API должен быть готов к работе до начала Sprint F2

