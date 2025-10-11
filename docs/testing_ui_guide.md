# Руководство по использованию Test UI в Cursor

Этот документ описывает, как использовать встроенный Test Explorer UI в Cursor/VS Code для запуска и визуализации результатов тестов.

## Настройка

Все необходимые настройки уже включены в проект:
- `.vscode/settings.json` - конфигурация pytest и Test Explorer
- `.vscode/tasks.json` - задачи для различных вариантов запуска тестов

## Использование Test Explorer UI

### Открытие панели тестов

1. **Через иконку**: Нажмите на иконку колбы (🧪) в боковой панели слева
2. **Через команду**: `Ctrl+Shift+P` → `Testing: Focus on Test Explorer View`
3. **Через меню**: View → Testing

### Основные возможности

#### 1. Автоматическое обнаружение тестов
- Тесты автоматически обнаруживаются при сохранении файлов
- Структура тестов отображается в виде дерева:
  ```
  tests/
  ├── test_conversation.py
  │   ├── test_add_and_get_history
  │   ├── test_history_limit
  │   └── ...
  └── test_settings.py
      ├── test_settings_with_required_fields
      └── ...
  ```

#### 2. Запуск тестов

**Из Test Explorer:**
- ▶️ **Запустить все тесты**: кнопка "Run All Tests" вверху панели
- ▶️ **Запустить файл**: нажмите кнопку запуска рядом с именем файла
- ▶️ **Запустить отдельный тест**: нажмите кнопку запуска рядом с именем теста
- 🐛 **Debug тест**: кнопка с иконкой bug для запуска в режиме отладки

**В редакторе кода:**
- Над каждым тестом появляются кнопки "Run Test" | "Debug Test"
- Можно запустить тест одним кликом прямо в коде

**Через Command Palette (`Ctrl+Shift+P`):**
- `Testing: Run All Tests`
- `Testing: Run Test at Cursor`
- `Testing: Debug Test at Cursor`

#### 3. Визуализация результатов

**Индикаторы статуса:**
- ✅ Зелёная галочка - тест пройден
- ❌ Красный крестик - тест провален
- ⏱️ Серый круг - тест не запускался
- 🔄 Синий круг - тест выполняется

**Детали результатов:**
- Кликните на тест в панели для просмотра деталей
- Вывод теста отображается в панели Terminal
- Для проваленных тестов показывается:
  - Сообщение об ошибке
  - Трейсбек
  - Ожидаемые vs фактические значения

**Цветовая подсветка в коде:**
- Зелёные/красные маркеры рядом с номерами строк показывают статус тестов

#### 4. Фильтрация тестов

В панели Test Explorer доступны фильтры:
- 🟢 Показать только пройденные тесты
- 🔴 Показать только проваленные тесты
- ⚪ Показать только не запущенные тесты

#### 5. Повторный запуск тестов

- **Последний запуск**: `Ctrl+; L` - повторить последний запуск
- **Только проваленные**: Кнопка "Run Failed Tests" - запустить только тесты, которые провалились

## Задачи VS Code Tasks

В дополнение к Test Explorer UI, доступны следующие задачи через `Ctrl+Shift+P` → `Tasks: Run Task`:

### Основные задачи

1. **Run Tests** (default test task)
   ```bash
   uv run pytest tests/ -v
   ```
   - Запускает все тесты с подробным выводом
   - Назначена как задача по умолчанию для группы "test"

2. **Run Tests with Coverage**
   ```bash
   uv run pytest tests/ --cov=src --cov-report=term-missing
   ```
   - Запускает тесты с анализом покрытия кода
   - Показывает, какие строки не покрыты тестами

3. **Run Tests with Coverage (HTML)**
   ```bash
   uv run pytest tests/ --cov=src --cov-report=html --cov-report=term-missing
   ```
   - Генерирует HTML отчёт о покрытии
   - Отчёт сохраняется в `htmlcov/index.html`
   - Откройте в браузере для детального просмотра

4. **Run Tests (Specific File)**
   ```bash
   uv run pytest ${file} -v
   ```
   - Запускает тесты только из текущего открытого файла
   - Полезно для быстрой проверки одного модуля

5. **Run Tests (Failed Only)**
   ```bash
   uv run pytest tests/ -v --lf
   ```
   - Запускает только тесты, которые провалились в прошлый раз
   - Флаг `--lf` (last failed) сохраняет состояние между запусками

6. **Run Tests (Verbose with Output)**
   ```bash
   uv run pytest tests/ -v -s
   ```
   - Запускает тесты с выводом print() и logging
   - Флаг `-s` отключает перехват stdout/stderr

### Быстрые клавиши

- `Ctrl+Shift+B` - запустить задачу по умолчанию (Run Bot)
- `Ctrl+Shift+T` - запустить тестовую задачу по умолчанию (Run Tests)

## Интеграция с другими инструментами

### Coverage Reports

После запуска тестов с покрытием (HTML):
```bash
# Windows
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

HTML отчёт показывает:
- Процент покрытия по файлам
- Какие строки покрыты (зелёные)
- Какие строки не покрыты (красные)
- Частично покрытые ветвления (жёлтые)

### Debugging Tests

1. Поставьте breakpoint в тесте (F9)
2. Нажмите кнопку "Debug Test" в коде или в Test Explorer
3. Используйте стандартные возможности отладки:
   - F10 - Step Over
   - F11 - Step Into
   - F5 - Continue
   - Просмотр переменных в панели Debug

### Continuous Testing

Для автоматического запуска тестов при изменениях:
```bash
uv run pytest tests/ -v --watch
```
Или используйте плагин `pytest-watch`:
```bash
uv add --dev pytest-watch
uv run ptw tests/
```

## Настройка конфигурации pytest

Конфигурация pytest находится в `pyproject.toml`:

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = "-v --strict-markers --tb=short"
```

### Полезные опции pytest

- `-v, --verbose` - подробный вывод
- `-s` - не перехватывать stdout/stderr
- `-x` - остановиться на первом провале
- `-k EXPRESSION` - запустить тесты, соответствующие выражению
- `--lf` - запустить только проваленные тесты
- `--ff` - сначала проваленные, потом остальные
- `--pdb` - открыть debugger при провале теста
- `--maxfail=N` - остановиться после N провалов
- `--tb=short` - краткий трейсбек (long, line, native, no)

### Примеры запуска с фильтрами

```bash
# Запустить только тесты с "settings" в имени
uv run pytest -k settings

# Запустить только тесты с "history" в имени
uv run pytest -k history

# Запустить тесты из конкретного файла и функции
uv run pytest tests/test_conversation.py::test_add_and_get_history

# Запустить с максимум 2 провалами
uv run pytest --maxfail=2
```

## Проблемы и решения

### Тесты не обнаруживаются

1. Проверьте, что pytest включен в settings:
   ```json
   "python.testing.pytestEnabled": true
   ```

2. Перезагрузите окно: `Ctrl+Shift+P` → `Developer: Reload Window`

3. Очистите кэш pytest:
   ```bash
   rm -rf .pytest_cache/
   ```

4. Проверьте Python Interpreter:
   - `Ctrl+Shift+P` → `Python: Select Interpreter`
   - Выберите интерпретатор из `.venv/`

### Тесты падают с ошибками импорта

1. Убедитесь, что в `settings.json` указан правильный путь:
   ```json
   "python.analysis.extraPaths": ["${workspaceFolder}/src"]
   ```

2. Проверьте, что `PYTHONPATH` включает `src/`:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:./src"
   ```

3. Используйте относительные импорты в тестах:
   ```python
   from config.settings import Settings
   # а не
   from src.config.settings import Settings
   ```

### Медленные тесты

1. Запускайте только изменённые тесты:
   ```bash
   uv run pytest --lf
   ```

2. Используйте параллельный запуск (требует pytest-xdist):
   ```bash
   uv add --dev pytest-xdist
   uv run pytest -n auto
   ```

3. Профилируйте тесты:
   ```bash
   uv run pytest --durations=10
   ```

## Дополнительные ресурсы

- [Pytest Documentation](https://docs.pytest.org/)
- [VS Code Python Testing](https://code.visualstudio.com/docs/python/testing)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)

## Чеклист качества тестов

✅ Все тесты проходят  
✅ Покрытие кода > 80%  
✅ Нет игнорируемых тестов без причины  
✅ Тесты быстрые (< 1 сек каждый)  
✅ Тесты изолированы (не зависят друг от друга)  
✅ Используются фикстуры для общей setup логики  
✅ Асинхронные тесты корректно помечены  
✅ Все edge cases покрыты  

