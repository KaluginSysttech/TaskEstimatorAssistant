# 🚀 Руководство по развертыванию TEA Bot

## Быстрый старт (Quick Start)

### Предварительные требования
- Python 3.10+
- Docker и Docker Compose
- uv (менеджер пакетов)

### Шаги развертывания

1. **Клонирование репозитория**
   ```bash
   git clone <repository-url>
   cd TEARepo
   ```

2. **Установка зависимостей**
   ```bash
   make setup
   # или
   uv pip install -e .
   ```

3. **Настройка переменных окружения**
   ```bash
   # Создайте файл .env в корне проекта
   cat > .env << EOF
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   OPENROUTER_API_KEY=your_openrouter_key_here
   DATABASE_URL=postgresql+asyncpg://telegrambot:telegrambot_password@localhost:5432/telegrambot
   OPENROUTER_MODEL=openai/gpt-3.5-turbo
   MAX_HISTORY_MESSAGES=20
   LLM_TIMEOUT=30
   LOG_LEVEL=INFO
   EOF
   ```

4. **Запуск PostgreSQL**
   ```bash
   docker-compose up -d
   ```

5. **Применение миграций**
   ```bash
   uv run alembic upgrade head
   ```

6. **Запуск бота**
   ```bash
   make run
   # или
   uv run python -m src.main
   ```

✅ **Готово!** Бот запущен и готов к работе.

---

## Детальное развертывание

### 1. Подготовка окружения

#### Установка Python 3.10+
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3.10 python3.10-venv

# Windows
# Скачайте с https://www.python.org/downloads/
```

#### Установка Docker
```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавьте пользователя в группу docker
sudo usermod -aG docker $USER
newgrp docker

# Windows/Mac
# Установите Docker Desktop с https://www.docker.com/products/docker-desktop
```

#### Установка uv
```bash
# Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Настройка базы данных

#### Запуск PostgreSQL
```bash
# Запустить контейнер
docker-compose up -d

# Проверить статус
docker-compose ps

# Просмотр логов
docker-compose logs -f postgres
```

#### Проверка подключения
```bash
# Подключиться к PostgreSQL
docker-compose exec postgres psql -U telegrambot -d telegrambot

# В psql:
\dt          # Список таблиц (после миграций)
\d users     # Структура таблицы users
\d messages  # Структура таблицы messages
\q           # Выход
```

#### Применение миграций
```bash
# Применить все миграции
uv run alembic upgrade head

# Проверить текущую версию
uv run alembic current

# История миграций
uv run alembic history
```

### 3. Получение API ключей

#### Telegram Bot Token
1. Откройте Telegram и найдите [@BotFather](https://t.me/BotFather)
2. Отправьте `/newbot`
3. Следуйте инструкциям
4. Скопируйте токен в формате `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`

#### OpenRouter API Key
1. Перейдите на [openrouter.ai](https://openrouter.ai/)
2. Зарегистрируйтесь или войдите
3. Перейдите в раздел "API Keys"
4. Создайте новый ключ
5. Скопируйте ключ в формате `sk-or-v1-...`

### 4. Конфигурация

#### Файл .env
```env
# === ОБЯЗАТЕЛЬНЫЕ ПАРАМЕТРЫ ===
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# === DATABASE (по умолчанию для Docker Compose) ===
DATABASE_URL=postgresql+asyncpg://telegrambot:telegrambot_password@localhost:5432/telegrambot

# === LLM НАСТРОЙКИ ===
OPENROUTER_MODEL=openai/gpt-3.5-turbo
LLM_TIMEOUT=30

# === ПРИЛОЖЕНИЕ ===
MAX_HISTORY_MESSAGES=20
LOG_LEVEL=INFO
TELEGRAM_MESSAGE_MAX_LENGTH=4000
```

#### Доступные модели LLM
- `openai/gpt-3.5-turbo` - быстро, дешево
- `openai/gpt-4` - качественнее, дороже
- `anthropic/claude-3-haiku` - альтернатива
- См. полный список на [openrouter.ai/models](https://openrouter.ai/models)

### 5. Запуск и мониторинг

#### Запуск бота
```bash
# Через Make
make run

# Напрямую
uv run python -m src.main

# В фоновом режиме (Linux/Mac)
nohup uv run python -m src.main > bot.log 2>&1 &
```

#### Просмотр логов
```bash
# Логи приложения
tail -f logs/app.log

# Только ошибки
tail -f logs/errors.log

# Логи PostgreSQL
docker-compose logs -f postgres
```

#### Остановка бота
```bash
# Ctrl+C в консоли

# Если запущен в фоне
pkill -f "python -m src.main"
```

#### Остановка PostgreSQL
```bash
# Остановить (данные сохраняются)
docker-compose stop

# Остановить и удалить контейнеры (данные в volume сохраняются)
docker-compose down

# Удалить ВСЁ включая данные (ОСТОРОЖНО!)
docker-compose down -v
```

---

## Обслуживание

### Бэкап базы данных
```bash
# Создать бэкап
docker-compose exec postgres pg_dump -U telegrambot telegrambot > backup_$(date +%Y%m%d_%H%M%S).sql

# Восстановить из бэкапа
docker-compose exec -T postgres psql -U telegrambot telegrambot < backup_20251016_123456.sql
```

### Миграции базы данных

#### Создание новой миграции
```bash
# Автогенерация после изменения моделей
uv run alembic revision --autogenerate -m "add new column"

# Проверьте сгенерированный файл в alembic/versions/
```

#### Применение миграций
```bash
# Применить все непримененные
uv run alembic upgrade head

# Применить конкретную версию
uv run alembic upgrade <revision_id>

# Откатить последнюю
uv run alembic downgrade -1
```

### Обновление зависимостей
```bash
# Обновить все зависимости
uv pip install --upgrade -e .

# Обновить конкретную зависимость
uv pip install --upgrade aiogram
```

### Очистка логов
```bash
# Архивировать старые логи
gzip logs/app.log
gzip logs/errors.log

# Очистить текущие
> logs/app.log
> logs/errors.log
```

---

## Troubleshooting

### Проблема: PostgreSQL не запускается
```bash
# Проверить статус
docker-compose ps

# Проверить логи
docker-compose logs postgres

# Решение: порт занят
# Измените порт в docker-compose.yml: "5433:5432"
# И обновите DATABASE_URL в .env: localhost:5433
```

### Проблема: Ошибка подключения к БД
```bash
# Проверка:
1. PostgreSQL запущен: docker-compose ps
2. Правильный DATABASE_URL в .env
3. Миграции применены: uv run alembic current

# Решение:
docker-compose restart
uv run alembic upgrade head
```

### Проблема: Бот не отвечает
```bash
# Проверка:
1. Правильный TELEGRAM_BOT_TOKEN в .env
2. Правильный OPENROUTER_API_KEY в .env
3. Проверить логи: tail -f logs/errors.log

# Тестирование токенов:
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
```

### Проблема: Миграции не применяются
```bash
# Проверить текущую версию
uv run alembic current

# Проверить историю
uv run alembic history

# Принудительно установить версию
uv run alembic stamp head

# Применить заново
uv run alembic upgrade head
```

---

## Production Deployment

### Systemd Service (Linux)

Создайте файл `/etc/systemd/system/tea-bot.service`:

```ini
[Unit]
Description=TEA Telegram Bot
After=network.target postgresql.service
Requires=postgresql.service

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/TEARepo
Environment="PATH=/home/ubuntu/.local/bin:/usr/bin"
ExecStart=/home/ubuntu/.local/bin/uv run python -m src.main
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Управление службой:
```bash
# Включить автозапуск
sudo systemctl enable tea-bot

# Запустить
sudo systemctl start tea-bot

# Статус
sudo systemctl status tea-bot

# Логи
sudo journalctl -u tea-bot -f

# Остановить
sudo systemctl stop tea-bot
```

### Docker Compose для продакшена

Обновите `docker-compose.yml` для продакшена:

```yaml
version: '3.8'

services:
  postgres:
    image: postgres:16-alpine
    container_name: telegram_bot_db
    environment:
      POSTGRES_USER: ${DB_USER:-telegrambot}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME:-telegrambot}
    ports:
      - "127.0.0.1:5432:5432"  # Только localhost
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U telegrambot"]
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  postgres_data:
```

### Безопасность

1. **Используйте сильные пароли** для PostgreSQL
2. **Ограничьте доступ** к порту 5432 (только localhost)
3. **Регулярно обновляйте** зависимости
4. **Настройте файрвол** на сервере
5. **Регулярные бэкапы** базы данных
6. **Мониторинг** логов и метрик

---

## Полезные команды

```bash
# Статус всех сервисов
docker-compose ps

# Перезапуск PostgreSQL
docker-compose restart postgres

# Просмотр использования ресурсов
docker stats

# Очистка Docker
docker system prune -a

# Проверка качества кода
make lint
make typecheck
make test

# Полная проверка
make quality
```

---

**Документация актуальна на**: 16.10.2025

