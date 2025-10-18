import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Строгая проверка типов
  typescript: {
    ignoreBuildErrors: false,
  },

  // Строгая проверка ESLint
  eslint: {
    ignoreDuringBuilds: false,
  },

  // Оптимизация production сборки
  reactStrictMode: true,

  // Переменные окружения для клиента
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001",
  },
};

export default nextConfig;
