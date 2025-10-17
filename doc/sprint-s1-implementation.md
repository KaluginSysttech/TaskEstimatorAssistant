# Sprint S1: Реализация персистентного хранилища

## Дата реализации
16.10.2025

## Цель
Заменить in-memory хранение диалогов на персистентное хранение в PostgreSQL с поддержкой сохранения истории между перезапусками бота.

## Что реализовано

### 1. База данных PostgreSQL
- **Docker Compose**: Настроен контейнер PostgreSQL 16 с автоматической инициализацией
- **Схема данных**:
  - Таблица `users`: хранение пользователей Telegram (telegram_id, username, created_at, is_deleted)
  - Таблица `messages`: хранение сообщений с метаданными (role, content, content_length, created_at, is_deleted)
- **Soft delete**: Все удаления выполняются через установку флага `is_deleted=True`

### 2. SQLAlchemy модели
- **src/db/models.py**: Определены модели User и Message с relationships
- **Async поддержка**: Все операции асинхронные через asyncpg
- **Метаданные**: Автоматическое заполнение `created_at` и `content_length`

### 3. Alembic миграции
- **Инициализация**: Настроен Alembic для async SQLAlchemy
- **Первая миграция**: `e7d81f36ca19_initial_schema.py` - создание базовой схемы
- **Конфигурация**: Чтение DATABASE_URL из переменных окружения

### 4. Repository слой
- **src/db/repository.py**: Класс `MessageRepository` с методами:
  - `get_or_create_user()`: Получение/создание пользователя
  - `add_message()`: Добавление сообщения с автоматическим вычислением длины
  - `get_history()`: Получение истории с лимитом и фильтрацией удалённых
  - `clear_history()`: Soft delete всех сообщений пользователя

### 5. Рефакторинг приложения
- **src/main.py**: 
  - Инициализация БД при запуске
  - Удалена зависимость от класса Conversation
  - Передача max_history_messages в MessageHandler
- **src/bot/message_handler.py**:
  - Использование MessageRepository вместо Conversation
  - Добавлен метод `handle_clear()` для команды /clear
  - Обновлена справка с упоминанием /clear
- **src/bot/telegram_bot.py**:
  - Зарегистрирован handler для команды /clear

### 6. Deprecation старого кода
- **src/llm/conversation.py**: Помечен как deprecated с предупреждением
- **src/llm/__init__.py**: Удалён экспорт Conversation

## Технические детали

### Зависимости (добавлены в pyproject.toml)
```toml
"sqlalchemy[asyncio]>=2.0.0"
"asyncpg>=0.29.0"
"alembic>=1.13.0"
```

### Конфигурация
Добавлено в `Settings`:
```python
database_url: str = Field(
    default="postgresql+asyncpg://telegrambot:telegrambot_password@localhost:5432/telegrambot",
    description="URL подключения к PostgreSQL",
)
```

### Команды для работы

#### Запуск PostgreSQL
```bash
docker-compose up -d
```

#### Создание миграции
```bash
uv run alembic revision --autogenerate -m "migration name"
```

#### Применение миграций
```bash
uv run alembic upgrade head
```

#### Откат миграции
```bash
uv run alembic downgrade -1
```

#### Остановка PostgreSQL
```bash
docker-compose down
```

## Архитектурные решения

1. **KISS принцип**: Простая схема БД без избыточных оптимизаций
2. **Async всюду**: Все операции с БД асинхронные для совместимости с aiogram
3. **Soft delete**: Физическое удаление не используется, что позволяет восстановить данные при необходимости
4. **Метаданные**: Автоматическое заполнение даты создания и длины сообщений
5. **Repository pattern**: Изоляция логики работы с БД от бизнес-логики

## Доступные команды бота

- `/start` - Приветственное сообщение
- `/help` - Справка
- `/role` - Роль и специализация бота
- `/clear` - Очистка истории диалога (новое!)

## Что не реализовано (потенциальные улучшения)

- Кэширование истории диалогов
- Индексы для оптимизации запросов (базовые есть, но можно добавить составные)
- Миграция данных из старого in-memory хранилища (не требуется, так как данные не сохранялись)
- Мониторинг производительности БД
- Бэкапы базы данных (можно настроить в docker-compose)

## Тестирование

Рекомендуется протестировать:
1. Создание нового пользователя при первом сообщении
2. Сохранение и загрузка истории диалога
3. Ограничение истории по max_history_messages
4. Команду /clear для очистки истории
5. Soft delete (проверить, что удалённые сообщения не загружаются)
6. Сохранение истории между перезапусками бота

## Статус
✅ Завершено

