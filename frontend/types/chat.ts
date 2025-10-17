/**
 * Chat-related TypeScript types
 * Sprint F4: AI Chat Implementation
 */

export type ChatMode = "normal" | "admin";
export type ChatRole = "user" | "assistant";

export interface ChatMessage {
    role: ChatRole;
    text: string;
    timestamp?: string;
}

export interface ChatMessageRequest {
    message: string;
    mode: ChatMode;
    session_id: string;
}

export interface ChatMessageResponse {
    response: string;
    mode: ChatMode;
    timestamp: string;
}

