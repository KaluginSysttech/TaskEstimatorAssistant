# 🚀 Quick Start - TEA Dashboard

## Запуск проекта (одна команда)

### Вариант 1: Через Makefile

```bash
# Запуск обоих сервисов параллельно
make run-dev-stack
```

**Примечание:** На Windows в PowerShell эта команда может не работать. Используйте Вариант 2.

---

### Вариант 2: Запуск вручную (Windows)

**Терминал 1 - Mock API:**
```bash
make run-stats-api
# или
uv run uvicorn src.api_main:app --host 0.0.0.0 --port 8001 --reload
```

**Терминал 2 - Frontend:**
```bash
make frontend-dev
# или
cd frontend
pnpm run dev
```

---

## URLs

После запуска откройте в браузере:

- **Dashboard:** http://localhost:3000
- **Mock API Swagger:** http://localhost:8001/docs
- **Mock API ReDoc:** http://localhost:8001/redoc

---

## Проверка статуса

### Проверка Mock API
```bash
curl http://localhost:8001/health
# PowerShell:
Invoke-WebRequest -Uri http://localhost:8001/health -UseBasicParsing
```

### Проверка Frontend
```bash
curl http://localhost:3000
# PowerShell:
Invoke-WebRequest -Uri http://localhost:3000 -UseBasicParsing
```

---

## Остановка сервисов

Нажмите `Ctrl+C` в окнах терминалов где запущены сервисы.

Или принудительно:
```powershell
# PowerShell
Get-Process | Where-Object {$_.ProcessName -match "python|node"} | Stop-Process -Force
```

---

## Устранение проблем

### Mock API не запускается

```bash
# Проверить что зависимости установлены
uv sync

# Проверить что порт 8001 свободен
netstat -ano | findstr :8001
```

### Frontend не запускается

```bash
# Переустановить зависимости
cd frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install

# Проверить что порт 3000 свободен
netstat -ano | findstr :3000
```

### Frontend показывает ошибки

Убедитесь что установлены все зависимости:
```bash
cd frontend
pnpm add @radix-ui/react-icons lucide-react
```

---

## Что должно быть видно

### Dashboard (http://localhost:3000)

✅ 4 KPI карточки с метриками  
✅ Селектор периода (день/неделя/месяц)  
✅ Список последних диалогов  
✅ Топ-5 пользователей  
✅ Placeholder для графика  

### Проверка работы

1. Откройте Dashboard
2. Измените период в селекторе - данные должны обновиться
3. Нажмите кнопку "Обновить" - данные должны перезагрузиться
4. Откройте Swagger UI и протестируйте API напрямую

---

## Быстрые команды

```bash
# Установка зависимостей
make setup              # Backend
make frontend-install   # Frontend

# Разработка
make run-stats-api     # Mock API
make frontend-dev      # Frontend

# Проверка качества
make frontend-lint      # ESLint
make frontend-typecheck # TypeScript

# Build
make frontend-build    # Production build
```

---

**Версия:** Sprint F2 Completed  
**Дата:** 2025-10-17

