/**
 * Floating Chat Button Component
 * Sprint F4: AI Chat Implementation
 */

"use client";

import { cn } from "@/lib/utils";
import { motion } from "framer-motion";
import { MessageCircle } from "lucide-react";

interface ChatFloatingButtonProps {
    onClick: () => void;
    isOpen: boolean;
    className?: string;
}

export function ChatFloatingButton({
    onClick,
    isOpen,
    className,
}: ChatFloatingButtonProps) {
    return (
        <motion.button
            onClick={onClick}
            className={cn(
                "fixed bottom-6 right-6 w-14 h-14 rounded-full",
                "bg-gradient-to-br from-blue-500 to-purple-600",
                "shadow-lg hover:shadow-xl",
                "flex items-center justify-center",
                "transition-all duration-200",
                "z-50",
                "focus:outline-none focus:ring-2 focus:ring-blue-400 focus:ring-offset-2",
                isOpen && "scale-0",
                className
            )}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.95 }}
            initial={{ scale: 0 }}
            animate={{ scale: isOpen ? 0 : 1 }}
            transition={{ duration: 0.2 }}
            title="Открыть чат"
        >
            <MessageCircle className="w-6 h-6 text-white" />

            {/* Pulse Animation Ring */}
            <motion.div
                className="absolute inset-0 rounded-full bg-blue-400/30"
                animate={{
                    scale: [1, 1.5, 1],
                    opacity: [0.5, 0, 0.5],
                }}
                transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeInOut",
                }}
            />
        </motion.button>
    );
}

