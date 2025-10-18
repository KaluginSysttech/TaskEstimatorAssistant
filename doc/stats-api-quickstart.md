# Statistics API - Quick Start Guide

## Обзор

Statistics API предоставляет данные для дашборда статистики проекта TEA. Текущая версия использует Mock реализацию с тестовыми данными.

**API URL:** `http://localhost:8001`  
**Документация:** http://localhost:8001/docs

## Быстрый старт

### 1. Установка зависимостей

```bash
uv sync
```

### 2. Запуск API

```bash
make run-stats-api
```

Или напрямую:

```bash
uv run uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload
```

API будет доступен на `http://localhost:8001`

### 3. Проверка работоспособности

```bash
# Health check
curl http://localhost:8001/health

# Или в PowerShell
Invoke-WebRequest -Uri "http://localhost:8001/health" -UseBasicParsing
```

## API Endpoints

### Health Check

**GET /** или **GET /health**

Проверка состояния API.

**Пример запроса:**
```bash
curl http://localhost:8001/health
```

**Пример ответа:**
```json
{
  "status": "healthy",
  "service": "TEA Statistics API",
  "version": "1.0.0",
  "implementation": "mock",
  "endpoints": {
    "stats": "/api/v1/stats?period={day|week|month}",
    "docs": "/docs",
    "redoc": "/redoc",
    "openapi": "/openapi.json"
  }
}
```

### Get Statistics

**GET /api/v1/stats**

Получить статистику за указанный период.

**Query параметры:**
- `period` (обязательный): `"day"`, `"week"`, или `"month"`

#### Пример 1: Статистика за день

```bash
curl "http://localhost:8001/api/v1/stats?period=day"
```

**PowerShell:**
```powershell
Invoke-WebRequest -Uri "http://localhost:8001/api/v1/stats?period=day" -UseBasicParsing | 
  Select-Object -ExpandProperty Content | 
  ConvertFrom-Json | 
  ConvertTo-Json -Depth 10
```

**Ответ:** Данные за последние 24 часа (по часам)

#### Пример 2: Статистика за неделю

```bash
curl "http://localhost:8001/api/v1/stats?period=week"
```

**Ответ:** Данные за последние 7 дней (по дням)

#### Пример 3: Статистика за месяц

```bash
curl "http://localhost:8001/api/v1/stats?period=month"
```

**Ответ:** Данные за последние 30 дней (по дням)

## Структура ответа

```json
{
  "period": "week",
  "summary": {
    "total_conversations": {
      "value": 964.0,
      "change_percent": 12.5,
      "trend": "up",
      "description": "Trending up this period"
    },
    "active_users": {
      "value": 121.0,
      "change_percent": -5.2,
      "trend": "down",
      "description": "Slightly decreased"
    },
    "avg_conversation_length": {
      "value": 8.4,
      "change_percent": 3.1,
      "trend": "up",
      "description": "Conversations are getting longer"
    },
    "growth_rate": {
      "value": 4.9,
      "change_percent": 0.8,
      "trend": "stable",
      "description": "Steady growth"
    }
  },
  "activity_chart": {
    "labels": ["2025-10-11", "2025-10-12", "...", "2025-10-17"],
    "values": [155.5, 189.6, 170.3, 152.6, 163.0, 101.8, 89.0]
  },
  "recent_conversations": [
    {
      "conversation_id": "conv_5118",
      "user_name": "Alice Smith",
      "started_at": "2025-10-17T10:22:46.141283",
      "message_count": 10,
      "status": "completed"
    }
  ],
  "top_users": [
    {
      "username": "demo_209",
      "conversation_count": 22,
      "message_count": 242,
      "last_active": "2025-10-17T03:05:46.141283"
    }
  ]
}
```

## Описание полей

### Summary (Сводная статистика)

Каждая метрика содержит:
- `value` - текущее значение
- `change_percent` - процент изменения относительно предыдущего периода
- `trend` - направление тренда: `"up"`, `"down"`, `"stable"`
- `description` - текстовое описание

**Метрики:**
- `total_conversations` - всего диалогов
- `active_users` - количество активных пользователей
- `avg_conversation_length` - средняя длина диалога (сообщений)
- `growth_rate` - скорость роста активности (%)

### Activity Chart (График активности)

- `labels` - временные метки:
  - `day`: часы (00:00, 01:00, ..., 23:00)
  - `week`: даты (2025-10-11, ..., 2025-10-17)
  - `month`: даты (30 дней)
- `values` - значения активности для каждой метки

### Recent Conversations (Последние диалоги)

Список из 10 последних диалогов:
- `conversation_id` - ID диалога
- `user_name` - имя пользователя
- `started_at` - время начала (ISO 8601)
- `message_count` - количество сообщений
- `status` - статус: `"active"` или `"completed"`

### Top Users (Топ пользователей)

Топ-5 наиболее активных пользователей:
- `username` - username пользователя
- `conversation_count` - количество диалогов
- `message_count` - количество сообщений
- `last_active` - последняя активность (ISO 8601)

## Тестирование

### Автоматическое тестирование

```bash
make test-stats-api
```

Эта команда протестирует все периоды (day, week, month) и выведет результаты.

### Интерактивная документация

Откройте Swagger UI для интерактивного тестирования:

```bash
make open-stats-docs
```

Или перейдите вручную: http://localhost:8001/docs

## Интеграция с фронтендом

### JavaScript/TypeScript

```typescript
const API_BASE_URL = 'http://localhost:8001';

async function getStats(period: 'day' | 'week' | 'month') {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/stats?period=${period}`
  );
  
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  
  return await response.json();
}

// Использование
const weekStats = await getStats('week');
console.log('Total conversations:', weekStats.summary.total_conversations.value);
```

### Python

```python
import requests

API_BASE_URL = 'http://localhost:8001'

def get_stats(period: str):
    response = requests.get(
        f'{API_BASE_URL}/api/v1/stats',
        params={'period': period}
    )
    response.raise_for_status()
    return response.json()

# Использование
week_stats = get_stats('week')
print('Total conversations:', week_stats['summary']['total_conversations']['value'])
```

## CORS

API настроен на прием запросов с любых источников (`allow_origins=["*"]`).

⚠️ **В production окружении** следует указать конкретные домены:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Коды ответов

- `200 OK` - успешный запрос
- `400 Bad Request` - невалидный параметр period
- `422 Unprocessable Entity` - ошибка валидации
- `500 Internal Server Error` - ошибка сервера

## Типы данных (TypeScript)

```typescript
type Trend = 'up' | 'down' | 'stable';
type Period = 'day' | 'week' | 'month';
type ConversationStatus = 'active' | 'completed';

interface MetricValue {
  value: number;
  change_percent: number;
  trend: Trend;
  description: string;
}

interface Summary {
  total_conversations: MetricValue;
  active_users: MetricValue;
  avg_conversation_length: MetricValue;
  growth_rate: MetricValue;
}

interface ActivityChart {
  labels: string[];
  values: number[];
}

interface RecentConversation {
  conversation_id: string;
  user_name: string;
  started_at: string; // ISO 8601
  message_count: number;
  status: ConversationStatus;
}

interface TopUser {
  username: string;
  conversation_count: number;
  message_count: number;
  last_active: string; // ISO 8601
}

interface StatsResponse {
  period: Period;
  summary: Summary;
  activity_chart: ActivityChart;
  recent_conversations: RecentConversation[];
  top_users: TopUser[];
}
```

## Troubleshooting

### API не запускается

1. Проверьте, что порт 8001 не занят:
   ```bash
   netstat -ano | findstr :8001
   ```

2. Проверьте, что зависимости установлены:
   ```bash
   uv sync
   ```

### Ошибка "Connection refused"

Убедитесь, что API запущен:
```bash
curl http://localhost:8001/health
```

### Данные не обновляются

Mock API использует фиксированный seed для генерации данных. Данные будут одинаковыми при каждом запросе с одним и тем же периодом.

## Дальнейшее развитие

### Sprint F5: Real API

В будущем Mock реализация будет заменена на реальную:
- Подключение к PostgreSQL базе данных
- Реальные данные из таблиц conversations, messages, users
- Кэширование для производительности
- Аутентификация и авторизация

Контракт API останется неизменным, фронтенд не потребует изменений.

## Полезные ссылки

- [План Sprint F1](sprint-f1-implementation.md)
- [Резюме Sprint F1](sprint-f1-summary.md)
- [Frontend Roadmap](frontend-roadmap.md)
- [OpenAPI Spec](http://localhost:8001/openapi.json)
- [ReDoc Documentation](http://localhost:8001/redoc)

---

**Версия:** 1.0.0  
**Дата:** 2025-10-17

