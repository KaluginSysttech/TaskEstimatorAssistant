/**
 * API client для работы с TEA Statistics Mock API
 */

import type { ChatMessageRequest, ChatMessageResponse } from "@/types/chat";
import type { APIError, Period, StatsResponse } from "@/types/stats";

/**
 * URL Mock API
 * В production это будет настраиваться через переменные окружения
 */
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8001";

/**
 * Класс ошибки API
 */
export class APIClientError extends Error {
    constructor(
        message: string,
        public statusCode?: number,
        public details?: APIError
    ) {
        super(message);
        this.name = "APIClientError";
    }
}

/**
 * Получить статистику за указанный период
 *
 * @param period - Период статистики ('day', 'week', 'month')
 * @returns Promise с данными статистики
 * @throws APIClientError при ошибке запроса
 */
export async function fetchStats(period: Period): Promise<StatsResponse> {
    const url = `${API_BASE_URL}/api/v1/stats?period=${period}`;

    try {
        const response = await fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
            // Отключаем кэширование для разработки
            cache: "no-store",
        });

        if (!response.ok) {
            const errorData: APIError = await response.json().catch(() => ({
                detail: "Unknown error",
            }));

            throw new APIClientError(
                `API request failed: ${response.statusText}`,
                response.status,
                errorData
            );
        }

        const data: StatsResponse = await response.json();
        return data;
    } catch (error) {
        // Если это уже наша ошибка, пробрасываем дальше
        if (error instanceof APIClientError) {
            throw error;
        }

        // Обрабатываем сетевые ошибки
        if (error instanceof TypeError) {
            throw new APIClientError(
                `Network error: Unable to connect to API at ${API_BASE_URL}. Make sure the Mock API is running.`,
                undefined,
                { detail: "Network error" }
            );
        }

        // Прочие неожиданные ошибки
        throw new APIClientError(
            `Unexpected error: ${error instanceof Error ? error.message : "Unknown error"}`,
            undefined,
            { detail: "Unexpected error" }
        );
    }
}

/**
 * Проверить доступность API (health check)
 *
 * @returns Promise<boolean> - true если API доступен
 */
export async function checkAPIHealth(): Promise<boolean> {
    try {
        const response = await fetch(`${API_BASE_URL}/health`, {
            method: "GET",
            cache: "no-store",
        });
        return response.ok;
    } catch {
        return false;
    }
}

/**
 * Отправить сообщение в чат
 *
 * @param request - Запрос с сообщением, режимом и session_id
 * @returns Promise с ответом от ассистента
 * @throws APIClientError при ошибке запроса
 */
export async function sendChatMessage(
    request: ChatMessageRequest
): Promise<ChatMessageResponse> {
    const url = `${API_BASE_URL}/api/v1/chat/message`;

    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(request),
            cache: "no-store",
        });

        if (!response.ok) {
            const errorData: APIError = await response.json().catch(() => ({
                detail: "Unknown error",
            }));

            throw new APIClientError(
                `Chat API request failed: ${response.statusText}`,
                response.status,
                errorData
            );
        }

        const data: ChatMessageResponse = await response.json();
        return data;
    } catch (error) {
        if (error instanceof APIClientError) {
            throw error;
        }

        if (error instanceof TypeError) {
            throw new APIClientError(
                `Network error: Unable to connect to Chat API at ${API_BASE_URL}`,
                undefined,
                { detail: "Network error" }
            );
        }

        throw new APIClientError(
            `Unexpected error: ${error instanceof Error ? error.message : "Unknown error"}`,
            undefined,
            { detail: "Unexpected error" }
        );
    }
}


