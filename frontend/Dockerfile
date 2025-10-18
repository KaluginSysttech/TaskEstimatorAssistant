FROM node:20-alpine

WORKDIR /app

# Установка pnpm
RUN corepack enable && corepack prepare pnpm@latest --activate

# Копирование package files
COPY package.json pnpm-lock.yaml ./

# Установка зависимостей
RUN pnpm install --frozen-lockfile

# Копирование исходного кода
COPY . .

# Открытие порта Next.js
EXPOSE 3000

# Запуск в dev режиме (для локальной разработки)
CMD ["pnpm", "dev"]

