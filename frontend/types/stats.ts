/**
 * TypeScript типы для TEA Statistics API
 * Основано на контракте Mock API из Sprint F1
 */

/**
 * Период статистики
 */
export type Period = "day" | "week" | "month";

/**
 * Направление тренда метрики
 */
export type Trend = "up" | "down" | "stable";

/**
 * Статус диалога
 */
export type ConversationStatus = "active" | "completed";

/**
 * Значение метрики с трендом
 */
export interface MetricValue {
    /** Числовое значение метрики */
    value: number;
    /** Процент изменения относительно предыдущего периода */
    change_percent: number;
    /** Направление тренда (вверх/вниз/стабильно) */
    trend: Trend;
    /** Текстовое описание тренда */
    description: string;
}

/**
 * Сводная статистика по ключевым метрикам
 */
export interface Summary {
    /** Всего диалогов за период */
    total_conversations: MetricValue;
    /** Количество активных пользователей */
    active_users: MetricValue;
    /** Средняя длина диалога (количество сообщений) */
    avg_conversation_length: MetricValue;
    /** Скорость роста активности (%) */
    growth_rate: MetricValue;
}

/**
 * Данные для графика активности
 */
export interface ActivityChart {
    /** Временные метки (даты или часы) */
    labels: string[];
    /** Значения активности для каждой метки */
    values: number[];
}

/**
 * Информация о недавнем диалоге
 */
export interface RecentConversation {
    /** Уникальный идентификатор диалога */
    conversation_id: string;
    /** Имя пользователя */
    user_name: string;
    /** Время начала диалога (ISO 8601) */
    started_at: string;
    /** Количество сообщений в диалоге */
    message_count: number;
    /** Статус диалога (active/completed) */
    status: ConversationStatus;
}

/**
 * Информация о топовом пользователе
 */
export interface TopUser {
    /** Username пользователя */
    username: string;
    /** Количество диалогов */
    conversation_count: number;
    /** Количество сообщений */
    message_count: number;
    /** Дата последней активности (ISO 8601) */
    last_active: string;
}

/**
 * Полный ответ API со статистикой
 */
export interface StatsResponse {
    /** Период статистики */
    period: Period;
    /** Сводная статистика */
    summary: Summary;
    /** Данные для графика активности */
    activity_chart: ActivityChart;
    /** Список последних диалогов (максимум 10) */
    recent_conversations: RecentConversation[];
    /** Топ-5 наиболее активных пользователей */
    top_users: TopUser[];
}

/**
 * Ошибка API
 */
export interface APIError {
    detail: string;
}


