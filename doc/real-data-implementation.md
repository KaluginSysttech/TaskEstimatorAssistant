# Подключение реальных данных из БД к дашборду

## Обзор

Дашборд теперь отображает **реальные данные из PostgreSQL** вместо mock-данных.

## Что было сделано

### 1. Создан RealStatCollector

Файл: `src/stats/real_collector.py`

Реализация сборщика статистики, который получает данные из БД через SQLAlchemy:
- Запросы к таблицам `users` и `messages`
- Расчет метрик за разные периоды (day/week/month)
- Сравнение с предыдущим периодом для трендов
- Агрегация данных для графиков активности

### 2. Обновлены зависимости

Файл: `src/api/dependencies.py`

- `get_stat_collector()` теперь асинхронная функция
- Возвращает `RealStatCollector` с сессией БД
- Интегрирована с `get_session()` для управления транзакциями

### 3. Обновлены API endpoints

Файлы:
- `src/api/stats_api.py` - добавлен `await` для `collector.get_stats()`
- `src/stats/collector.py` - Protocol обновлен для async метода

### 4. Обновлен AdminHandler

Файл: `src/chat/admin_handler.py`

- Все вызовы `stat_collector.get_stats()` теперь с `await`
- Обновлен текст: "Данные получены из базы данных в реальном времени"

### 5. Создан скрипт для seed данных

Файл: `scripts/seed_test_data.py`

Генерирует тестовые данные:
- 10 пользователей
- ~4000 сообщений за 30 дней
- Реалистичное распределение по времени (больше активности в рабочие дни)

## Метрики из БД

### Summary Metrics

**Total Conversations:**
```sql
SELECT COUNT(DISTINCT user_id) as total_conversations
FROM messages
WHERE created_at >= :start_date
  AND is_deleted = FALSE
```

**Active Users:**
```sql
SELECT COUNT(DISTINCT u.id) as active_users
FROM users u
JOIN messages m ON u.id = m.user_id
WHERE m.created_at >= :start_date
  AND m.is_deleted = FALSE
  AND u.is_deleted = FALSE
```

**Average Conversation Length:**
```sql
SELECT COUNT(m.id) / COUNT(DISTINCT m.user_id) as avg_length
FROM messages m
WHERE m.created_at >= :start_date
  AND m.is_deleted = FALSE
```

### Activity Chart

Агрегирует количество сообщений по временным интервалам:
- **Day**: по часам (24 точки)
- **Week**: по дням (7 точек)
- **Month**: по дням (30 точек)

### Recent Conversations

Последние 10 пользователей с их активностью:
```sql
SELECT 
    u.id,
    u.username,
    u.telegram_id,
    MIN(m.created_at) as started_at,
    COUNT(m.id) as message_count,
    MAX(m.created_at) as last_message_at
FROM users u
JOIN messages m ON u.id = m.user_id
WHERE u.is_deleted = FALSE
  AND m.is_deleted = FALSE
GROUP BY u.id, u.username, u.telegram_id
ORDER BY MAX(m.created_at) DESC
LIMIT 10
```

### Top Users

Топ-5 пользователей по активности за период:
```sql
SELECT 
    u.username,
    u.telegram_id,
    COUNT(m.id) as message_count,
    MAX(m.created_at) as last_active
FROM users u
JOIN messages m ON u.id = m.user_id
WHERE u.is_deleted = FALSE
  AND m.is_deleted = FALSE
  AND m.created_at >= :start_date
GROUP BY u.id, u.username, u.telegram_id
ORDER BY COUNT(m.id) DESC
LIMIT 5
```

## Как использовать

### Просмотр дашборда

1. Откройте http://localhost:3000
2. Выберите период (Day/Week/Month)
3. Дашборд отобразит реальные данные из БД

### Добавление новых данных

Запустите скрипт seed:
```bash
uv run python scripts/seed_test_data.py
```

### Admin Mode чата

1. Откройте чат (синяя кнопка справа внизу)
2. Переключите на Admin Mode (зеленая иконка 📊)
3. Спросите: "Сколько диалогов было на этой неделе?"
4. Получите ответ с реальными данными из БД

## Производительность

- Все запросы используют индексы на `created_at` и `user_id`
- Асинхронные запросы не блокируют event loop
- Данные не кэшируются (real-time)

## Следующие шаги

Возможные улучшения:
- [ ] Добавить кэширование статистики (Redis)
- [ ] Оптимизировать запросы через materialized views
- [ ] Добавить фильтры по пользователям
- [ ] Экспорт статистики в CSV/Excel
- [ ] Real-time обновление через WebSocket

## Тестовые данные

После запуска seed скрипта:
- **Пользователи**: alice_dev, bob_tester, charlie_user, diana_admin, eve_customer, frank_support, grace_team, henry_qa, ivy_manager, jack_engineer
- **Период**: последние 30 дней
- **Сообщения**: ~4000 сообщений с реалистичным распределением

## Архитектура

```
Frontend (Next.js)
    ↓
API Endpoint (/api/v1/stats)
    ↓
RealStatCollector
    ↓
PostgreSQL Database
    ↓
users + messages tables
```

## Обратная совместимость

Mock данные все еще доступны через `MockStatCollector`:
```python
# В dependencies.py можно вернуться к mock
from src.stats.mock_collector import MockStatCollector

def get_stat_collector():
    return MockStatCollector(seed=42)
```

