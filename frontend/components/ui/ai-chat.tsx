/**
 * AI Chat Component
 * Based on 21st.dev reference, adapted for TEA project
 * Sprint F4: AI Chat Implementation
 */

"use client";

import { useChat } from "@/hooks/use-chat";
import { cn } from "@/lib/utils";
import { AnimatePresence, motion } from "framer-motion";
import { BarChart3, Bot, Send, X } from "lucide-react";
import { useEffect, useRef } from "react";

interface AIChatProps {
    className?: string;
    isOpen: boolean;
    onClose: () => void;
}

export function AIChat({ className, isOpen, onClose }: AIChatProps) {
    const {
        messages,
        input,
        setInput,
        isTyping,
        mode,
        toggleMode,
        sendMessage,
        error,
    } = useChat();

    const messagesEndRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    }, [messages]);

    const handleSend = () => {
        if (!input.trim()) return;
        sendMessage();
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    // Mode-specific styling
    const modeConfig = {
        normal: {
            color: "blue",
            icon: Bot,
            label: "Обычный режим",
            description: "Общение с LLM-ассистентом",
            bgGradient: "from-blue-500/20 via-black to-gray-900",
            borderColor: "border-blue-500/20",
        },
        admin: {
            color: "green",
            icon: BarChart3,
            label: "Режим администратора",
            description: "Вопросы по статистике",
            bgGradient: "from-green-500/20 via-black to-gray-900",
            borderColor: "border-green-500/20",
        },
    };

    const config = modeConfig[mode];
    const ModeIcon = config.icon;

    if (!isOpen) return null;

    return (
        <AnimatePresence>
            <motion.div
                initial={{ opacity: 0, scale: 0.8, y: 20 }}
                animate={{ opacity: 1, scale: 1, y: 0 }}
                exit={{ opacity: 0, scale: 0.8, y: 20 }}
                transition={{ duration: 0.2 }}
                className={cn(
                    "fixed bottom-24 right-6 w-[360px] h-[500px] rounded-2xl overflow-hidden shadow-2xl z-50",
                    "md:w-[400px] md:h-[600px]",
                    className
                )}
            >
                {/* Animated Outer Border */}
                <motion.div
                    className={cn(
                        "absolute inset-0 rounded-2xl border-2",
                        config.borderColor
                    )}
                    animate={{ rotate: [0, 360] }}
                    transition={{ duration: 25, repeat: Infinity, ease: "linear" }}
                />

                {/* Inner Card */}
                <div className="relative flex flex-col w-full h-full rounded-xl border border-white/10 overflow-hidden bg-black/95 backdrop-blur-xl">
                    {/* Inner Animated Background */}
                    <motion.div
                        className={cn("absolute inset-0 bg-gradient-to-br", config.bgGradient)}
                        animate={{ backgroundPosition: ["0% 0%", "100% 100%", "0% 0%"] }}
                        transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                        style={{ backgroundSize: "200% 200%" }}
                    />

                    {/* Floating Particles */}
                    {Array.from({ length: 15 }).map((_, i) => (
                        <motion.div
                            key={i}
                            className="absolute w-1 h-1 rounded-full bg-white/10"
                            animate={{
                                y: ["0%", "-140%"],
                                x: [Math.random() * 200 - 100, Math.random() * 200 - 100],
                                opacity: [0, 1, 0],
                            }}
                            transition={{
                                duration: 5 + Math.random() * 3,
                                repeat: Infinity,
                                delay: i * 0.5,
                                ease: "easeInOut",
                            }}
                            style={{ left: `${Math.random() * 100}%`, bottom: "-10%" }}
                        />
                    ))}

                    {/* Header */}
                    <div className="px-4 py-3 border-b border-white/10 relative z-10 flex items-center justify-between">
                        <div className="flex items-center gap-2">
                            <ModeIcon className="w-5 h-5 text-white" />
                            <div>
                                <h2 className="text-sm font-semibold text-white">{config.label}</h2>
                                <p className="text-xs text-white/60">{config.description}</p>
                            </div>
                        </div>
                        <div className="flex items-center gap-2">
                            {/* Mode Toggle */}
                            <button
                                onClick={toggleMode}
                                className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
                                title={`Переключить на ${mode === "normal" ? "режим администратора" : "обычный режим"}`}
                            >
                                {mode === "normal" ? (
                                    <BarChart3 className="w-4 h-4 text-green-400" />
                                ) : (
                                    <Bot className="w-4 h-4 text-blue-400" />
                                )}
                            </button>
                            {/* Close Button */}
                            <button
                                onClick={onClose}
                                className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors"
                                title="Закрыть чат"
                            >
                                <X className="w-4 h-4 text-white" />
                            </button>
                        </div>
                    </div>

                    {/* Messages */}
                    <div className="flex-1 px-4 py-3 overflow-y-auto space-y-3 text-sm flex flex-col relative z-10">
                        {messages.length === 0 && (
                            <div className="flex items-center justify-center h-full text-white/60 text-center px-4">
                                <div>
                                    <ModeIcon className="w-12 h-12 mx-auto mb-3 opacity-50" />
                                    <p className="text-sm">
                                        {mode === "normal"
                                            ? "Начните диалог с ассистентом"
                                            : "Задайте вопрос о статистике диалогов"}
                                    </p>
                                </div>
                            </div>
                        )}

                        {messages.map((msg, i) => (
                            <motion.div
                                key={i}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ duration: 0.4 }}
                                className={cn(
                                    "px-3 py-2 rounded-xl max-w-[85%] shadow-md backdrop-blur-md break-words",
                                    msg.role === "assistant"
                                        ? "bg-white/10 text-white self-start"
                                        : "bg-white/30 text-black font-medium self-end"
                                )}
                            >
                                <div className="whitespace-pre-wrap">{msg.text}</div>
                                {msg.timestamp && (
                                    <div
                                        className={cn(
                                            "text-xs mt-1 opacity-60",
                                            msg.role === "assistant" ? "text-white" : "text-black"
                                        )}
                                    >
                                        {new Date(msg.timestamp).toLocaleTimeString("ru-RU", {
                                            hour: "2-digit",
                                            minute: "2-digit",
                                        })}
                                    </div>
                                )}
                            </motion.div>
                        ))}

                        {/* AI Typing Indicator */}
                        {isTyping && (
                            <motion.div
                                className="flex items-center gap-2 px-3 py-2 rounded-xl max-w-[30%] bg-white/10 self-start"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: [0, 1, 0.6, 1] }}
                                transition={{ repeat: Infinity, duration: 1.2 }}
                            >
                                <span className="w-2 h-2 rounded-full bg-white animate-pulse"></span>
                                <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-200"></span>
                                <span className="w-2 h-2 rounded-full bg-white animate-pulse delay-400"></span>
                            </motion.div>
                        )}

                        {/* Error Message */}
                        {error && (
                            <div className="px-3 py-2 rounded-xl bg-red-500/20 border border-red-500/40 text-red-200 text-xs">
                                {error}
                            </div>
                        )}

                        <div ref={messagesEndRef} />
                    </div>

                    {/* Input */}
                    <div className="flex items-center gap-2 p-3 border-t border-white/10 relative z-10">
                        <input
                            className="flex-1 px-3 py-2 text-sm bg-black/50 rounded-lg border border-white/10 text-white placeholder:text-white/40 focus:outline-none focus:ring-1 focus:ring-white/50"
                            placeholder={
                                mode === "normal"
                                    ? "Напишите сообщение..."
                                    : "Спросите о статистике..."
                            }
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            disabled={isTyping}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || isTyping}
                            className="p-2 rounded-lg bg-white/10 hover:bg-white/20 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                            <Send className="w-4 h-4 text-white" />
                        </button>
                    </div>
                </div>
            </motion.div>
        </AnimatePresence>
    );
}

