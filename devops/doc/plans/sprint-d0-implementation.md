# Sprint D0 - Basic Docker Setup - Implementation

## Статус: ✅ Completed

**Дата завершения:** 18 октября 2025

## Обзор

Реализована базовая Docker инфраструктура для локального запуска всех сервисов проекта TEA одной командой `docker-compose up`.

## Выполненные задачи

### ✅ 1. Создание .dockerignore файлов

**Файлы:**
- `.dockerignore` (корневой) - для Bot и API сервисов
- `frontend/.dockerignore` - для Frontend сервиса

**Исключены:**
- Python временные файлы (__pycache__, *.pyc)
- Node modules и build артефакты
- Переменные окружения (.env)
- IDE конфигурация
- Логи и тесты
- Документация

### ✅ 2. Создание Dockerfile для Bot

**Файл:** `Dockerfile.bot`

**Технологии:**
- Base image: `python:3.11-slim`
- Package manager: `uv`
- Запуск: `uv run python -m src.main`

**Структура:**
```dockerfile
FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
COPY src/ ./src/
COPY prompts/ ./prompts/
COPY alembic/ ./alembic/
COPY alembic.ini ./
CMD ["uv", "run", "python", "-m", "src.main"]
```

### ✅ 3. Создание Dockerfile для API

**Файл:** `Dockerfile.api`

**Технологии:**
- Base image: `python:3.11-slim`
- Package manager: `uv`
- Запуск: `uvicorn` на порту 8001

**Отличия от Bot:**
- Открывает порт 8001
- Не требует prompts/ директории
- Запускается через uvicorn

### ✅ 4. Создание Dockerfile для Frontend

**Файл:** `frontend/Dockerfile`

**Технологии:**
- Base image: `node:20-alpine`
- Package manager: `pnpm`
- Режим: Development (`pnpm dev`)
- Порт: 3000

**Особенности:**
- Использует corepack для установки pnpm
- Hot-reload через volume mount
- Frozen lockfile для детерминированной установки

### ✅ 5. Обновление docker-compose.yml

**Добавлено 3 новых сервиса:**

1. **bot** - Telegram бот
   - Зависит от postgres (healthcheck)
   - Переменные окружения из .env
   - Volume для логов: `./logs:/app/logs`

2. **api** - FastAPI сервер
   - Зависит от postgres (healthcheck)
   - Порт: 8001
   - Те же переменные окружения что у бота

3. **frontend** - Next.js приложение
   - Зависит от api
   - Порт: 3000
   - Volume для hot-reload
   - Environment: NEXT_PUBLIC_API_URL

**Healthcheck для PostgreSQL:**
```yaml
healthcheck:
  test: ["CMD-SHELL", "pg_isready -U telegrambot"]
  interval: 10s
  timeout: 5s
  retries: 5
```

**Порядок запуска:**
1. PostgreSQL (с healthcheck)
2. Bot и API (ждут healthy postgres)
3. Frontend (ждет api)

### ✅ 6. Обновление README.md

**Добавлен раздел "🐳 Запуск через Docker":**

Содержание:
- Быстрый старт (3 простых шага)
- Требования и настройка .env
- Проверка работоспособности
- Управление сервисами (up -d, logs, down, rebuild)
- Применение миграций БД
- Таблица структуры сервисов
- Troubleshooting (3 типичные проблемы)

**Добавлен badge:**
```markdown
[![Docker](https://img.shields.io/badge/docker-ready-blue.svg)](https://www.docker.com/)
```

## Критерии приёмки

| Критерий | Статус |
|----------|--------|
| Все 4 сервиса запускаются командой `docker-compose up` | ✅ |
| PostgreSQL готов к работе до запуска Bot и API | ✅ |
| Bot подключается к Telegram и БД | ✅ |
| API доступен на http://localhost:8001/docs | ✅ |
| Frontend доступен на http://localhost:3000 | ✅ |
| Логи пишутся в директорию `logs/` | ✅ |
| Hot-reload работает для frontend | ✅ |
| .dockerignore исключает ненужные файлы | ✅ |
| README.md содержит инструкции по Docker | ✅ |

## Структура созданных файлов

```
TEARepo/
├── .dockerignore                          # NEW ✅
├── Dockerfile.bot                         # NEW ✅
├── Dockerfile.api                         # NEW ✅
├── frontend/
│   ├── .dockerignore                      # NEW ✅
│   └── Dockerfile                         # NEW ✅
├── docker-compose.yml                     # UPDATED ✅
└── README.md                              # UPDATED ✅
```

## Команда запуска

```bash
# Создать .env файл с токенами
TELEGRAM_BOT_TOKEN=your_token
OPENROUTER_API_KEY=your_key

# Запустить все сервисы
docker-compose up

# В отдельном терминале применить миграции
docker-compose exec bot uv run alembic upgrade head
```

## Результат

✅ **Все сервисы успешно запускаются одной командой**

**Доступные URL:**
- Frontend: http://localhost:3000
- API Docs: http://localhost:8001/docs
- PostgreSQL: localhost:5432

## Что НЕ включено (Future work)

Следующие оптимизации запланированы на последующие спринты:

- ❌ Multi-stage builds (D1)
- ❌ Production конфигурация (D2)
- ❌ CI/CD для автоматической сборки образов (D1)
- ❌ Публикация образов в GitHub Container Registry (D1)
- ❌ Автоматические миграции при запуске (D2)
- ❌ Healthchecks для Bot и API (D2)
- ❌ Hadolint проверки Dockerfile (D1)

## Примечания

### MVP подход

Использован минимально функциональный подход:
- Простые single-stage Dockerfile
- Dev режим для frontend (быстрый hot-reload)
- Без оптимизации размера образов
- Без production-specific настроек

### Преимущества текущей реализации

1. **Быстрый старт** - одна команда для запуска всех сервисов
2. **Изоляция** - каждый сервис в своем контейнере
3. **Детерминизм** - frozen lockfiles гарантируют одинаковые зависимости
4. **Надежность** - healthcheck и depends_on обеспечивают правильный порядок запуска
5. **Удобство разработки** - hot-reload для frontend, volume для логов

### Технические детали

**Healthcheck для PostgreSQL:**
- Проверяет готовность БД перед запуском сервисов
- Интервал: 10 секунд
- Timeout: 5 секунд
- Retries: 5 попыток

**Environment переменные:**
- Передаются из .env файла через docker-compose
- DATABASE_URL хардкодится для контейнеров (service name "postgres")
- Default values в docker-compose.yml для опциональных переменных

**Volumes:**
- `./logs:/app/logs` - доступ к логам бота
- `./frontend:/app` - hot-reload для frontend
- `/app/node_modules` - предотвращение конфликтов с хост-системой

## Следующие шаги

1. **Sprint D1** - Build & Publish
   - Настройка GitHub Actions для автоматической сборки
   - Публикация образов в ghcr.io
   - Multi-stage builds для оптимизации

2. **Sprint D2** - Развертывание на сервер
   - Production docker-compose.yml
   - Инструкции по ручному развертыванию

3. **Sprint D3** - Auto Deploy
   - Автоматизация деплоя через GitHub Actions
   - Workflow dispatch для ручного триггера

