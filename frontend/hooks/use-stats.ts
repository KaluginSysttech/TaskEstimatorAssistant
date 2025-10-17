"use client";

/**
 * React hook для получения статистики из API
 */

import { APIClientError, fetchStats } from "@/lib/api";
import type { Period, StatsResponse } from "@/types/stats";
import { useCallback, useEffect, useState } from "react";

/**
 * Состояние hook'а
 */
interface UseStatsState {
    /** Данные статистики */
    data: StatsResponse | null;
    /** Флаг загрузки */
    loading: boolean;
    /** Ошибка, если есть */
    error: string | null;
}

/**
 * Возвращаемое значение hook'а
 */
interface UseStatsReturn extends UseStatsState {
    /** Функция для принудительного обновления данных */
    refetch: () => void;
}

/**
 * Hook для получения статистики диалогов
 *
 * @param period - Период статистики ('day', 'week', 'month')
 * @returns Объект с данными, состоянием загрузки, ошибкой и функцией обновления
 *
 * @example
 * ```tsx
 * function Dashboard() {
 *   const { data, loading, error, refetch } = useStats('week');
 *
 *   if (loading) return <div>Загрузка...</div>;
 *   if (error) return <div>Ошибка: {error}</div>;
 *   if (!data) return null;
 *
 *   return <div>{data.summary.total_conversations.value}</div>;
 * }
 * ```
 */
export function useStats(period: Period): UseStatsReturn {
    const [state, setState] = useState<UseStatsState>({
        data: null,
        loading: true,
        error: null,
    });

    const loadStats = useCallback(async () => {
        setState((prev) => ({ ...prev, loading: true, error: null }));

        try {
            const data = await fetchStats(period);
            setState({
                data,
                loading: false,
                error: null,
            });
        } catch (err) {
            const errorMessage =
                err instanceof APIClientError
                    ? err.message
                    : "Произошла неизвестная ошибка";

            setState({
                data: null,
                loading: false,
                error: errorMessage,
            });

            // Логируем ошибку в консоль для разработки
            console.error("Failed to fetch stats:", err);
        }
    }, [period]);

    // Загружаем данные при монтировании и изменении периода
    useEffect(() => {
        loadStats();
    }, [loadStats]);

    // Функция для принудительного обновления
    const refetch = useCallback(() => {
        loadStats();
    }, [loadStats]);

    return {
        ...state,
        refetch,
    };
}


