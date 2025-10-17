# Sprint F4: Quick Start Guide - AI Chat

Быстрый старт для тестирования функциональности AI чата.

## Предварительные требования

1. **Backend зависимости установлены:**
   ```bash
   uv sync --all-extras
   ```

2. **Frontend зависимости установлены:**
   ```bash
   cd frontend && pnpm install
   ```

3. **База данных:**
   - PostgreSQL запущен (или используется SQLite)
   - Миграции применены:
     ```bash
     uv run alembic upgrade head
     ```

4. **.env файл настроен:**
   ```env
   OPENROUTER_API_KEY=your_api_key_here
   MODEL_NAME=anthropic/claude-3-haiku
   DATABASE_URL=postgresql+asyncpg://...
   ```

## Запуск

### Вариант 1: Full Stack (рекомендуется)

```bash
# В корневой директории проекта
make run-dev-stack
```

Это запустит:
- Backend API на http://localhost:8001
- Frontend на http://localhost:3000

### Вариант 2: Раздельный запуск

**Terminal 1 - Backend:**
```bash
make run-stats-api
# или
uv run uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload
```

**Terminal 2 - Frontend:**
```bash
make frontend-dev
# или
cd frontend && pnpm run dev
```

## Тестирование

### 1. Проверка API

Откройте http://localhost:8001/docs

Найдите endpoint **POST /api/v1/chat/message** и протестируйте:

**Request (Normal Mode):**
```json
{
  "message": "Привет! Кто ты?",
  "mode": "normal",
  "session_id": "test-session-123"
}
```

**Request (Admin Mode):**
```json
{
  "message": "Сколько диалогов было на этой неделе?",
  "mode": "admin",
  "session_id": "test-session-123"
}
```

### 2. Проверка UI

1. Откройте http://localhost:3000
2. В правом нижнем углу увидите **синюю floating button** с иконкой сообщения
3. Кликните на кнопку - откроется чат

**Тестирование Normal Mode (синий):**
- По умолчанию чат открывается в обычном режиме
- Иконка: 🤖 Bot
- Цвет: синий
- Отправьте сообщение: "Привет! Расскажи о себе"
- Ожидаемый результат: ответ от LLM-ассистента о его роли

**Тестирование Admin Mode (зеленый):**
- Кликните на иконку **BarChart3** (справа от заголовка)
- Режим переключится на администратора
- Иконка: 📊 BarChart3
- Цвет: зеленый

Попробуйте следующие запросы:
```
1. "Сколько диалогов было на этой неделе?"
2. "Покажи активных пользователей"
3. "Общая статистика за месяц"
4. "Динамика активности за неделю"
```

Ожидаемый результат: mock-ответы с данными из StatCollector

### 3. Проверка Session Persistence

1. Отправьте несколько сообщений в чате
2. Закройте чат (кнопка X)
3. Откройте чат снова
4. Отправьте новое сообщение
5. **Ожидаемый результат:** История сохранилась (сообщения загружаются из БД)

### 4. Проверка адаптивности

- Откройте DevTools (F12)
- Переключите на мобильный вид
- Проверьте, что чат корректно отображается
- Floating button должна быть видна

## Возможные проблемы и решения

### 1. "Network error: Unable to connect to Chat API"

**Причина:** Backend API не запущен

**Решение:**
```bash
make run-stats-api
```

### 2. "LLM API error"

**Причина:** Неверный или отсутствующий OPENROUTER_API_KEY

**Решение:**
- Проверьте `.env` файл
- Убедитесь, что API key действителен
- Проверьте баланс в OpenRouter

### 3. "Database connection error"

**Причина:** БД не запущена или миграции не применены

**Решение:**
```bash
# Запустите PostgreSQL или используйте SQLite
# Примените миграции
uv run alembic upgrade head
```

### 4. Admin mode не отвечает на запросы

**Причина:** Mock data не сгенерирован

**Решение:**
- Admin mode использует MockStatCollector
- Данные генерируются автоматически
- Проверьте консоль backend на ошибки

## Примеры запросов для Admin Mode

**Статистика диалогов:**
```
- "Сколько диалогов было сегодня?"
- "Количество диалогов за неделю"
- "Всего диалогов за месяц"
```

**Активные пользователи:**
```
- "Покажи активных пользователей"
- "Кто самые активные пользователи?"
- "Топ пользователей за неделю"
```

**Общая статистика:**
```
- "Общая статистика"
- "Покажи метрики за неделю"
- "Статистика за месяц"
```

**Динамика активности:**
```
- "Динамика активности"
- "График активности за неделю"
- "Как изменялась активность?"
```

## Структура проекта

```
TEARepo/
├── src/
│   ├── api/
│   │   ├── chat_api.py          # Chat API endpoint
│   │   ├── models.py            # Pydantic models
│   │   └── dependencies.py      # DI для chat
│   ├── chat/
│   │   ├── chat_handler.py      # Main handler
│   │   └── admin_handler.py     # Admin mode handler
│   ├── db/
│   │   ├── models.py            # ChatSession, ChatMessage
│   │   └── repository.py        # ChatRepository
│   └── api_main.py              # FastAPI app
├── frontend/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── ai-chat.tsx      # Chat component
│   │   │   └── chat-floating-button.tsx
│   │   └── layout/
│   │       └── dashboard-layout.tsx
│   ├── hooks/
│   │   └── use-chat.ts          # Chat hook
│   ├── types/
│   │   └── chat.ts              # TypeScript types
│   └── lib/
│       └── api.ts               # API client
└── doc/
    ├── sprint-f4-implementation.md
    └── sprint-f4-quickstart.md
```

## Логирование и отладка

### Backend логи

```bash
# Запустите API с подробным логированием
uv run uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload --log-level debug
```

Логи покажут:
- Входящие запросы
- Обработку сообщений (mode, session_id)
- Взаимодействие с LLM
- Сохранение в БД

### Frontend логи

Откройте DevTools Console (F12) и проверьте:
- Network requests к `/api/v1/chat/message`
- Ошибки при отправке сообщений
- Session ID generation

## Следующие шаги

После успешного тестирования:

1. **Кастомизация промпта:**
   - Отредактируйте `prompts/system_prompt.txt`
   - Перезапустите backend

2. **Настройка admin mode:**
   - Модифицируйте `src/chat/admin_handler.py`
   - Добавьте новые типы запросов

3. **Sprint F5:**
   - Переход на Real StatCollector
   - Real text-to-SQL для admin mode
   - Расширенная аналитика

## Полезные ссылки

- **API Documentation:** http://localhost:8001/docs
- **ReDoc:** http://localhost:8001/redoc
- **Frontend:** http://localhost:3000
- **Implementation Guide:** [sprint-f4-implementation.md](sprint-f4-implementation.md)
- **Frontend Roadmap:** [frontend-roadmap.md](frontend-roadmap.md)

## Поддержка

Если возникли проблемы:
1. Проверьте логи backend и frontend
2. Убедитесь, что все зависимости установлены
3. Проверьте конфигурацию в `.env`
4. Просмотрите [sprint-f4-implementation.md](sprint-f4-implementation.md)

---

**Дата:** 2025-10-17  
**Спринт:** F4 - Реализация ИИ-чата  
**Версия:** 1.0

