# Frontend Vision: TEA Dashboard

## Обзор

Frontend приложение для визуализации статистики диалогов Telegram-бота TEA (Task Estimation Assistant). Представляет собой современный веб-дашборд, построенный на Next.js с TypeScript.

## Цели проекта

### Основные
- **Визуализация статистики** - отображение ключевых метрик работы бота
- **Простота использования** - интуитивный интерфейс без лишних элементов
- **Производительность** - быстрая загрузка и отзывчивость интерфейса
- **Масштабируемость** - готовность к добавлению новых функций

### Технические
- Типобезопасность через TypeScript
- Современный UI/UX с shadcn/ui
- Server-side rendering для оптимизации SEO
- Легкая интеграция с Backend API

## Технологический стек

### Основа
- **Next.js 15** - React фреймворк с App Router
- **TypeScript** - строгая типизация
- **React 19** - UI библиотека

### Стилизация
- **Tailwind CSS** - utility-first CSS фреймворк
- **shadcn/ui** - коллекция готовых компонентов
- **CSS Variables** - темизация и кастомизация

### Инструменты разработки
- **pnpm** - быстрый пакетный менеджер
- **ESLint** - линтинг кода
- **TypeScript Compiler** - проверка типов

## Архитектурные принципы

### 1. KISS (Keep It Simple, Stupid)
- Минимум абстракций
- Прямолинейная структура кода
- Нет оверинжиниринга

### 2. Компонентная архитектура
- Переиспользуемые UI компоненты
- Изолированная логика
- Props drilling при необходимости (без глобального стейта пока не нужен)

### 3. Типобезопасность
- Все функции и компоненты типизированы
- Интерфейсы для API responses
- Никаких `any` типов

### 4. Server-First подход
- Использование Server Components где возможно
- Client Components только для интерактивности
- RSC (React Server Components) по умолчанию

## Структура проекта

```
frontend/
├── app/                      # Next.js App Router
│   ├── layout.tsx           # Корневой layout
│   ├── page.tsx             # Главная страница (дашборд)
│   ├── globals.css          # Глобальные стили
│   └── api/                 # API routes (опционально)
├── components/
│   ├── ui/                  # shadcn/ui компоненты
│   ├── dashboard/           # Компоненты дашборда
│   │   ├── stat-card.tsx
│   │   ├── activity-chart.tsx
│   │   ├── recent-conversations.tsx
│   │   └── top-users.tsx
│   └── layout/              # Layout компоненты
│       ├── header.tsx
│       └── sidebar.tsx
├── lib/
│   ├── utils.ts             # Утилиты (cn, clsx)
│   └── api.ts               # API client
├── types/
│   └── stats.ts             # TypeScript типы для API
├── hooks/
│   └── use-stats.ts         # Custom hooks
├── public/                  # Статические файлы
└── doc/                     # Документация
```

## Соглашения по коду

### Именование файлов
- Компоненты: `kebab-case.tsx` (например: `stat-card.tsx`)
- Утилиты: `kebab-case.ts` (например: `api-client.ts`)
- Типы: `kebab-case.ts` (например: `stats.ts`)

### Именование компонентов
- PascalCase для React компонентов
- camelCase для функций и переменных
- UPPER_CASE для констант

### Структура компонентов

```typescript
// 1. Импорты
import React from 'react';
import { Button } from '@/components/ui/button';

// 2. Типы
interface ComponentProps {
  title: string;
  value: number;
}

// 3. Компонент
export function Component({ title, value }: ComponentProps) {
  return (
    <div>
      <h3>{title}</h3>
      <p>{value}</p>
    </div>
  );
}
```

### TypeScript правила
- Явное указание типов для props
- Return типы для функций (опционально, inference работает хорошо)
- Интерфейсы вместо type aliases для объектов (предпочтительно)
- Избегать `any`, использовать `unknown` если тип неизвестен

## State Management

### Текущий подход (Sprint F2-F3)
- **React useState** - для локального состояния компонентов
- **Server Components** - для данных, не требующих интерактивности
- **Custom hooks** - для переиспользуемой логики (useStats)

### Будущее (при необходимости)
- Zustand - легковесный state manager
- React Context - для темизации и глобальных настроек
- TanStack Query - для кэширования API запросов

## Интеграция с Backend

### Mock API (Sprint F2-F4)
- **URL:** `http://localhost:8001/api/v1/stats`
- **Метод:** GET
- **Параметры:** `?period=day|week|month`

### API Client
```typescript
// lib/api.ts
export async function fetchStats(period: Period): Promise<StatsResponse> {
  const response = await fetch(`${API_URL}/api/v1/stats?period=${period}`);
  if (!response.ok) throw new Error('Failed to fetch stats');
  return response.json();
}
```

### Error Handling
- Try-catch блоки в async функциях
- Error boundaries для React компонентов (будущее)
- Пользовательские сообщения об ошибках
- Fallback UI при ошибках загрузки

## UI/UX принципы

### Дизайн система
- **shadcn/ui** - базовые компоненты
- **Tailwind CSS** - кастомная стилизация
- **Стиль:** New York (более минималистичный)
- **Цветовая схема:** Slate (нейтральная, профессиональная)

### Адаптивность
- Mobile-first подход
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Гибкие grid layouts

### Доступность
- Семантический HTML
- ARIA атрибуты где необходимо
- Keyboard navigation
- Цветовой контраст

## Производительность

### Оптимизации
- **Server Components** - меньше JavaScript на клиенте
- **Code splitting** - автоматически через Next.js
- **Image optimization** - через next/image
- **Font optimization** - через next/font

### Метрики
- First Contentful Paint (FCP) < 1.5s
- Time to Interactive (TTI) < 3.0s
- Lighthouse Score > 90

## Тестирование

### Текущий спринт (F2)
- Ручное тестирование
- TypeScript проверка типов
- ESLint проверка кода

### Будущее
- Jest + React Testing Library - unit тесты
- Playwright - E2E тесты
- Storybook - компонентная документация

## Процесс разработки

### Workflow
1. Создать компонент в соответствующей директории
2. Добавить типы в types/
3. Реализовать логику
4. Протестировать в браузере
5. Проверить типы: `pnpm run type-check`
6. Проверить линтинг: `pnpm run lint`

### Команды
```bash
pnpm run dev          # Запуск dev сервера
pnpm run build        # Production build
pnpm run lint         # Проверка ESLint
pnpm run type-check   # Проверка TypeScript
```

## Дорожная карта развития

### Sprint F2 (Текущий)
- ✅ Инициализация проекта
- ✅ Настройка инструментов
- ✅ Базовая структура

### Sprint F3
- Dashboard компоненты
- Интеграция с Mock API
- Визуализация данных

### Sprint F4
- AI Chat интерфейс
- WebSocket соединение (возможно)
- Админ-панель

### Sprint F5
- Переход на Real API
- Оптимизация производительности
- Production deployment

## Безопасность

### Текущие меры
- TypeScript защита от runtime ошибок
- ESLint правила безопасности
- HTTPS в production (будущее)

### Будущие меры
- CSP (Content Security Policy)
- Rate limiting на клиенте
- Input validation
- XSS protection

## Документация

### Обязательная документация
- README.md - общая информация и quick start
- Этот файл (front-vision.md) - архитектурные решения
- Комментарии в коде для сложной логики

### Опциональная документация
- Storybook для компонентов (будущее)
- API documentation (автогенерация из TypeScript типов)

## Интеграция с основным проектом

### Связь с Backend
- Backend на Python (FastAPI)
- Frontend на Node.js (Next.js)
- Разные репозитории/директории, но единый проект
- Общий Docker compose для dev окружения (будущее)

### Deployment
- Backend: отдельный сервер/контейнер
- Frontend: Vercel / Netlify / собственный сервер
- Nginx как reverse proxy (опционально)

## Ограничения и допущения

### Текущие ограничения
- Нет аутентификации (пока не требуется)
- Нет real-time обновлений (polling или manual refresh)
- Только desktop-first (mobile будет оптимизирован позже)

### Технический долг
- Нет unit тестов (пока)
- Нет E2E тестов (пока)
- Нет компонентной документации (Storybook)

## Заключение

Данная концепция описывает архитектуру и принципы разработки frontend приложения TEA Dashboard. Документ является живым и будет обновляться по мере развития проекта.

**Принципы:**
- Простота превыше всего (KISS)
- Типобезопасность обязательна
- Производительность важна
- Масштабируемость необходима

**Цель:** Создать качественный, поддерживаемый и расширяемый frontend для визуализации статистики TEA бота.

---

**Версия:** 1.0  
**Дата:** 2025-10-17  
**Спринт:** F2 - Инициализация Frontend проекта  
**Статус:** 📋 Текущий документ


