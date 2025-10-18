# TEA Frontend - Dashboard

> Веб-дашборд для визуализации статистики диалогов Telegram-бота TEA (Task Estimation Assistant)

[![Next.js](https://img.shields.io/badge/Next.js-15-black)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-blue)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-blue)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-4-06B6D4)](https://tailwindcss.com/)
[![shadcn/ui](https://img.shields.io/badge/shadcn%2Fui-latest-black)](https://ui.shadcn.com/)

---

## 📖 О проекте

Frontend приложение для отображения статистики работы TEA бота. Построено на современном стеке технологий с упором на производительность, типобезопасность и качество кода.

### Основные возможности

- 📊 **Ключевые метрики (KPI)** - сводная статистика по диалогам
- 📈 **График активности** - визуализация данных за различные периоды
- 💬 **Последние диалоги** - список недавних взаимодействий
- 👥 **Топ пользователи** - наиболее активные пользователи
- 🔄 **Переключение периодов** - день, неделя, месяц
- ⚡ **Real-time обновление** - кнопка обновления данных

---

## 🛠️ Технологический стек

### Основа
| Технология | Версия | Назначение |
|------------|--------|------------|
| **Next.js** | 15.x | React фреймворк с App Router |
| **React** | 19.x | UI библиотека |
| **TypeScript** | 5.x | Статическая типизация |
| **pnpm** | 10.x | Пакетный менеджер |

### Стилизация и UI
| Технология | Версия | Назначение |
|------------|--------|------------|
| **Tailwind CSS** | 4.x | Utility-first CSS фреймворк |
| **shadcn/ui** | latest | Коллекция готовых компонентов |
| **Radix UI** | latest | Headless UI primitives |
| **Lucide React** | latest | Иконки |

### Инструменты разработки
| Технология | Назначение |
|------------|------------|
| **ESLint** | Линтинг кода |
| **TypeScript Compiler** | Проверка типов |
| **Turbopack** | Быстрый bundler для dev/build |

---

## 📋 Требования

Перед установкой убедитесь, что у вас есть:

- ✅ **Node.js** 20.x или выше
- ✅ **pnpm** 10.x или выше
- ✅ **Mock API** запущен на `http://localhost:8001` (из Sprint F1)

### Установка pnpm

Если pnpm не установлен:

```bash
# Windows (PowerShell)
iwr https://get.pnpm.io/install.ps1 -useb | iex

# macOS / Linux
curl -fsSL https://get.pnpm.io/install.sh | sh -

# Или через npm
npm install -g pnpm
```

---

## 🚀 Быстрый старт

### 1. Установка зависимостей

```bash
# Из корня репозитория
make frontend-install

# Или напрямую из frontend директории
cd frontend
pnpm install
```

### 2. Запуск Mock API (обязательно!)

```bash
# В отдельном терминале, из корня репозитория
make run-stats-api
```

API будет доступен на `http://localhost:8001`

### 3. Запуск frontend dev сервера

```bash
# Из корня репозитория
make frontend-dev

# Или напрямую из frontend директории
cd frontend
pnpm run dev
```

Приложение откроется на `http://localhost:3000`

### 4. Запуск всего стека сразу

```bash
# Запустить Mock API + Frontend одной командой
make run-dev-stack
```

---

## 💻 Команды разработки

### Основные команды (из корня репозитория)

```bash
# Установка зависимостей
make frontend-install

# Запуск dev сервера
make frontend-dev

# Production build
make frontend-build

# Линтинг
make frontend-lint

# Проверка типов
make frontend-typecheck

# Запуск всего стека (API + Frontend)
make run-dev-stack
```

### Команды из директории frontend

```bash
# Запуск dev сервера
pnpm run dev

# Production build
pnpm run build

# Запуск production сборки
pnpm run start

# Линтинг
pnpm run lint

# Проверка типов
pnpm run type-check
```

---

## 📁 Структура проекта

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Корневой layout
│   ├── page.tsx             # Главная страница (дашборд)
│   └── globals.css          # Глобальные стили
├── components/
│   ├── ui/                  # shadcn/ui компоненты (автогенерация)
│   ├── dashboard/           # Компоненты дашборда (Sprint F3)
│   └── layout/              # Layout компоненты (Sprint F3)
├── lib/
│   ├── utils.ts             # Утилиты (cn функция)
│   └── api.ts               # API client для Mock API
├── types/
│   └── stats.ts             # TypeScript типы для API
├── hooks/
│   └── use-stats.ts         # React hook для получения статистики
├── doc/
│   └── front-vision.md      # Архитектурная концепция
├── public/                  # Статические файлы
├── components.json          # Конфигурация shadcn/ui
├── tailwind.config.ts       # Конфигурация Tailwind
├── tsconfig.json            # Конфигурация TypeScript
├── next.config.ts           # Конфигурация Next.js
├── .eslintrc.json           # Конфигурация ESLint
├── package.json             # Зависимости
└── README.md                # Этот файл
```

---

## 🔧 Конфигурация

### Переменные окружения

Создайте файл `.env.local` в директории `frontend/`:

```env
# URL Mock API (по умолчанию: http://localhost:8001)
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Порты

- **Frontend**: `http://localhost:3000`
- **Mock API**: `http://localhost:8001`

Порты можно изменить:

```bash
# Frontend - другой порт
pnpm run dev -- -p 3001

# Mock API - изменить в src/api_main.py или команде запуска
```

---

## 🏗️ Архитектура

### Принципы

- **KISS** - минимум абстракций, простой и понятный код
- **Типобезопасность** - все функции и компоненты типизированы
- **Server-First** - использование Server Components где возможно
- **Component-Driven** - переиспользуемые изолированные компоненты

### Ключевые компоненты

#### API Client (`lib/api.ts`)
```typescript
// Получение статистики
const data = await fetchStats('week');
```

#### React Hook (`hooks/use-stats.ts`)
```typescript
// В компоненте
const { data, loading, error, refetch } = useStats('week');
```

#### TypeScript типы (`types/stats.ts`)
```typescript
// Полная типизация API контракта
interface StatsResponse {
  period: Period;
  summary: Summary;
  activity_chart: ActivityChart;
  recent_conversations: RecentConversation[];
  top_users: TopUser[];
}
```

---

## 🎨 Дизайн система

### shadcn/ui

Используется **New York** стиль с **Slate** цветовой схемой.

Установленные компоненты:
- `Card` - карточки для контента
- `Button` - кнопки
- `Badge` - бейджи для статусов и трендов
- `Select` - селектор периода

Добавление новых компонентов:

```bash
cd frontend
pnpm dlx shadcn@latest add [component-name]
```

### Tailwind CSS

Конфигурация в `tailwind.config.ts`. Используется Tailwind v4 с CSS Variables для темизации.

---

## 🧪 Тестирование

### Текущий этап (Sprint F2)
- ✅ Ручное тестирование в браузере
- ✅ TypeScript проверка типов (`pnpm run type-check`)
- ✅ ESLint проверка кода (`pnpm run lint`)

### Будущее (Sprint F3+)
- Unit тесты (Jest + React Testing Library)
- E2E тесты (Playwright)
- Component документация (Storybook)

---

## 🐛 Отладка

### Проблемы с подключением к API

**Ошибка:** `Network error: Unable to connect to API`

**Решение:**
1. Убедитесь, что Mock API запущен (`make run-stats-api`)
2. Проверьте, что API доступен: `curl http://localhost:8001/health`
3. Проверьте переменную окружения `NEXT_PUBLIC_API_URL`

### Проблемы с зависимостями

**Ошибка:** `Cannot find module '@/...'`

**Решение:**
```bash
# Переустановить зависимости
cd frontend
rm -rf node_modules pnpm-lock.yaml
pnpm install
```

### Проблемы с типами

**Ошибка:** TypeScript ошибки компиляции

**Решение:**
```bash
# Проверка типов
cd frontend
pnpm run type-check

# Пересоздать типы
rm -rf .next
pnpm run dev
```

---

## 📚 Полезные ссылки

### Документация проекта
- [Frontend Vision](doc/front-vision.md) - архитектурная концепция
- [Main README](../README.md) - основной README проекта
- [Frontend Roadmap](../doc/frontend-roadmap.md) - план развития frontend

### Документация технологий
- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev/)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com/)

### Курсы и туториалы
- [Next.js Learn](https://nextjs.org/learn)
- [React Beta Docs](https://react.dev/learn)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/)

---

## 🤝 Разработка

### Соглашения по коду

#### Файлы и папки
- Компоненты: `kebab-case.tsx` (например: `stat-card.tsx`)
- Хуки: `use-*.ts` (например: `use-stats.ts`)
- Типы: `kebab-case.ts` (например: `stats.ts`)

#### Именование
- Компоненты: `PascalCase`
- Функции: `camelCase`
- Константы: `UPPER_CASE`
- Типы: `PascalCase`

#### TypeScript
- Явное указание типов для props
- Избегать `any`, использовать `unknown`
- Интерфейсы для объектов

### Процесс разработки

1. Создать feature branch
2. Написать код с типами
3. Проверить типы: `pnpm run type-check`
4. Проверить линтинг: `pnpm run lint`
5. Протестировать в браузере
6. Создать PR

---

## 📊 Статус проекта

### ✅ Sprint F2 (Текущий) - Completed
- Инициализация Next.js проекта
- Настройка shadcn/ui и Tailwind CSS
- TypeScript типы для API
- API client и React hook
- Базовая страница дашборда

### 🚧 Sprint F3 (Следующий)
- Полноценные компоненты дашборда
- График активности (Chart.js или Recharts)
- Продвинутая визуализация данных

### 📋 Sprint F4
- AI Chat интерфейс
- Admin функционал

### 🎯 Sprint F5
- Переход на Real API
- Production оптимизация

---

## 📄 Лицензия

Часть проекта TEA (Task Estimation Assistant). MVP для проверки идеи.

---

## 📞 Поддержка

По вопросам и предложениям создавайте Issues в репозитории.

---

**Версия:** 1.0  
**Дата:** 2025-10-17  
**Спринт:** F2 - Инициализация Frontend проекта  
**Статус:** ✅ Completed
