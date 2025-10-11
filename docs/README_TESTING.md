# 🧪 Документация по тестированию

> Центральная точка входа для всей документации по тестированию проекта TEA

## 📚 Структура документации

```
docs/
├── 🚀 test_ui_quickstart.md      ← НАЧНИТЕ ОТСЮДА!
├── 📚 testing_ui_guide.md         ← Полное руководство
├── 📋 test_ui_setup_summary.md    ← Что было настроено
└── 📖 README_TESTING.md           ← Этот файл
```

---

## 🎯 Выберите свой путь

### 🚀 "Хочу быстро начать!"

**→ [`test_ui_quickstart.md`](test_ui_quickstart.md)**

- ⏱️ Время чтения: 2 минуты
- 🎯 Цель: Запустить тесты за 30 секунд
- 📋 Содержание:
  - Как открыть Test Explorer
  - Как запустить тесты
  - Горячие клавиши
  - Типичные сценарии

### 📚 "Хочу разобраться во всём!"

**→ [`testing_ui_guide.md`](testing_ui_guide.md)**

- ⏱️ Время чтения: 15-20 минут
- 🎯 Цель: Стать экспертом в Test UI
- 📋 Содержание:
  - Все возможности Test Explorer
  - Интеграция с pytest
  - Debugging
  - Coverage reports
  - Troubleshooting
  - Best practices

### 📋 "Что было настроено?"

**→ [`test_ui_setup_summary.md`](test_ui_setup_summary.md)**

- ⏱️ Время чтения: 5 минут
- 🎯 Цель: Понять изменения в проекте
- 📋 Содержание:
  - Список изменённых файлов
  - Новые задачи VS Code
  - Примеры использования
  - Чеклист проверки

---

## 📊 Текущее состояние тестов

### ✅ Статистика (по состоянию на последний запуск)

```
Всего тестов:    16
Пройдено:        16 (100%)
Провалено:       0 (0%)
Время:           0.79s
```

### 📈 Покрытие кода

```
Модуль                      Покрытие    Статус
─────────────────────────────────────────────────
src/config/settings.py      100%        ✅ Отлично
src/llm/conversation.py     100%        ✅ Отлично
src/llm/__init__.py         100%        ✅ Отлично
src/llm/llm_client.py        17%        ⚠️ Требует внимания
src/bot/message_handler.py   0%         ❌ Не покрыто
src/bot/telegram_bot.py       0%         ❌ Не покрыто
src/main.py                   0%         ❌ Не покрыто
─────────────────────────────────────────────────
ИТОГО:                       19%        ⚠️ Нужны тесты
```

> 💡 **Note:** Для MVP 19% - приемлемо. Критические модули (settings, conversation) покрыты на 100%.

---

## 🛠️ Быстрые команды

### Через командную строку

```bash
# Все тесты
make test

# С покрытием
uv run pytest tests/ --cov=src --cov-report=term-missing

# HTML отчёт покрытия
uv run pytest tests/ --cov=src --cov-report=html
# Открыть: start htmlcov/index.html

# Только проваленные
uv run pytest tests/ --lf

# С выводом print()
uv run pytest tests/ -v -s

# Конкретный тест
uv run pytest tests/test_conversation.py::test_add_and_get_history
```

### Через Test Explorer UI

1. Откройте панель Testing (🧪 в боковой панели)
2. Кликните на тест → ▶️ Run или 🐛 Debug
3. Результаты отобразятся автоматически

### Через Tasks (Ctrl+Shift+P → Tasks: Run Task)

- `Run Tests` - стандартный запуск
- `Run Tests with Coverage` - с анализом покрытия
- `Run Tests with Coverage (HTML)` - HTML отчёт
- `Run Tests (Specific File)` - только текущий файл
- `Run Tests (Failed Only)` - только проваленные
- `Run Tests (Verbose with Output)` - с print()

---

## 🎓 Обучающие материалы

### Для начинающих

1. **Прочитайте:** [`test_ui_quickstart.md`](test_ui_quickstart.md)
2. **Попробуйте:**
   - Откройте Test Explorer (🧪)
   - Запустите все тесты (▶️ Run All Tests)
   - Кликните на любой тест для деталей
3. **Изучите:** горячие клавиши (`Ctrl+;` + буква)

### Для продвинутых

1. **Прочитайте:** [`testing_ui_guide.md`](testing_ui_guide.md)
2. **Попробуйте:**
   - Debug тест с breakpoint (F9 → 🐛)
   - Запустите тесты с покрытием (HTML)
   - Создайте свой тест
3. **Изучите:** все задачи VS Code

### Для экспертов

1. **Настройте:** `.vscode/settings.json` под свои нужды
2. **Создайте:** свои задачи в `.vscode/tasks.json`
3. **Интегрируйте:** с CI/CD pipeline
4. **Оптимизируйте:** покрытие кода до >80%

---

## 🔗 Внешние ресурсы

### Официальная документация

- [VS Code Python Testing](https://code.visualstudio.com/docs/python/testing)
- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

### Полезные статьи

- [Testing Best Practices](https://docs.pytest.org/en/latest/explanation/goodpractices.html)
- [VS Code Testing Features](https://code.visualstudio.com/docs/editor/testing)
- [Python Testing Guide](https://realpython.com/pytest-python-testing/)

---

## 📝 Чеклист для новых разработчиков

Перед началом работы убедитесь, что:

- [ ] Прочитали [`test_ui_quickstart.md`](test_ui_quickstart.md)
- [ ] Открыли Test Explorer (🧪) и видите все тесты
- [ ] Запустили все тесты (▶️) и видите 16/16 passed
- [ ] Попробовали debug тест (F9 → 🐛)
- [ ] Знаете горячие клавиши (`Ctrl+;` + A/C/D/F/L)
- [ ] Попробовали задачи VS Code (Ctrl+Shift+P → Tasks)
- [ ] Запустили тесты с покрытием (HTML)

---

## 🆘 Проблемы?

### Тесты не видны в Test Explorer

1. `Ctrl+Shift+P` → `Developer: Reload Window`
2. Проверьте Python Interpreter: `Ctrl+Shift+P` → `Python: Select Interpreter`
3. Выберите интерпретатор из `.venv/`
4. Проверьте, что pytest установлен: `uv run pytest --version`

### Ошибки импорта в тестах

1. Проверьте `.vscode/settings.json`:
   ```json
   "python.analysis.extraPaths": ["${workspaceFolder}/src"]
   ```
2. Проверьте `sys.path` в тестах
3. Используйте относительные импорты

### Медленные тесты

1. Запускайте только изменённые: `pytest --lf`
2. Используйте параллельный запуск: `pytest -n auto` (требует pytest-xdist)
3. Профилируйте: `pytest --durations=10`

### Другие проблемы

📖 См. раздел "Проблемы и решения" в [`testing_ui_guide.md`](testing_ui_guide.md)

---

## 🎯 Цели на будущее

### Краткосрочные (MVP)
- [x] Настроить Test Explorer UI
- [x] Покрыть тестами критические модули (settings, conversation)
- [ ] Добавить тесты для bot модулей
- [ ] Достичь 50% покрытия

### Долгосрочные (Production)
- [ ] Достичь 80%+ покрытия
- [ ] Интеграция с CI/CD
- [ ] Автоматический запуск тестов на pre-commit
- [ ] Mutation testing
- [ ] Performance testing
- [ ] Integration tests для Telegram API

---

## 📞 Поддержка

По вопросам о тестировании:
1. Сначала проверьте эту документацию
2. Затем [`testing_ui_guide.md`](testing_ui_guide.md) - раздел Troubleshooting
3. Создайте Issue в репозитории

---

**Последнее обновление:** October 2025  
**Версия:** 1.0  
**Статус:** ✅ Production Ready  

---

## 🎉 Приятного тестирования!

> "Код без тестов - код, который работает только у вас на машине" © Мудрый разработчик

