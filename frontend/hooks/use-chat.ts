/**
 * Custom hook for chat functionality
 * Sprint F4: AI Chat Implementation
 */

"use client";

import { sendChatMessage } from "@/lib/api";
import type { ChatMessage, ChatMode } from "@/types/chat";
import { useCallback, useEffect, useState } from "react";

/**
 * Generate or retrieve session ID from localStorage
 */
function getSessionId(): string {
    if (typeof window === "undefined") return "";

    const storageKey = "tea-chat-session-id";
    let sessionId = localStorage.getItem(storageKey);

    if (!sessionId) {
        // Generate UUID v4
        sessionId = crypto.randomUUID();
        localStorage.setItem(storageKey, sessionId);
    }

    return sessionId;
}

export function useChat() {
    const [messages, setMessages] = useState<ChatMessage[]>([]);
    const [input, setInput] = useState("");
    const [isTyping, setIsTyping] = useState(false);
    const [mode, setMode] = useState<ChatMode>("normal");
    const [sessionId, setSessionId] = useState("");
    const [error, setError] = useState<string | null>(null);

    // Initialize session ID on mount
    useEffect(() => {
        setSessionId(getSessionId());
    }, []);

    // Send message to API
    const sendMessage = useCallback(
        async (messageText?: string) => {
            const text = messageText || input;
            if (!text.trim() || !sessionId) return;

            // Add user message
            const userMessage: ChatMessage = {
                role: "user",
                text: text.trim(),
                timestamp: new Date().toISOString(),
            };
            setMessages((prev) => [...prev, userMessage]);
            setInput("");
            setIsTyping(true);
            setError(null);

            try {
                // Call API
                const response = await sendChatMessage({
                    message: text.trim(),
                    mode,
                    session_id: sessionId,
                });

                // Add assistant message
                const assistantMessage: ChatMessage = {
                    role: "assistant",
                    text: response.response,
                    timestamp: response.timestamp,
                };
                setMessages((prev) => [...prev, assistantMessage]);
            } catch (err) {
                // Handle error
                const errorMessage =
                    err instanceof Error ? err.message : "Произошла ошибка при отправке сообщения";
                setError(errorMessage);

                // Add error message to chat
                const errorChatMessage: ChatMessage = {
                    role: "assistant",
                    text: `❌ ${errorMessage}`,
                    timestamp: new Date().toISOString(),
                };
                setMessages((prev) => [...prev, errorChatMessage]);
            } finally {
                setIsTyping(false);
            }
        },
        [input, mode, sessionId]
    );

    // Toggle mode
    const toggleMode = useCallback(() => {
        setMode((prev) => (prev === "normal" ? "admin" : "normal"));
    }, []);

    // Clear history (local only - backend history persists)
    const clearMessages = useCallback(() => {
        setMessages([]);
        setError(null);
    }, []);

    // Reset session (generate new session ID)
    const resetSession = useCallback(() => {
        if (typeof window !== "undefined") {
            localStorage.removeItem("tea-chat-session-id");
            const newSessionId = getSessionId();
            setSessionId(newSessionId);
            setMessages([]);
            setError(null);
        }
    }, []);

    return {
        messages,
        input,
        setInput,
        isTyping,
        mode,
        toggleMode,
        sendMessage,
        clearMessages,
        resetSession,
        error,
    };
}

