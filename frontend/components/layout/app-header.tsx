"use client";

import { Button } from "@/components/ui/button";
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select";
import type { Period } from "@/types/stats";
import { Github, Menu, RefreshCw } from "lucide-react";

interface AppHeaderProps {
    period: Period;
    onPeriodChange: (period: Period) => void;
    onRefresh: () => void;
    onMenuClick: () => void;
}

export function AppHeader({
    period,
    onPeriodChange,
    onRefresh,
    onMenuClick,
}: AppHeaderProps) {
    return (
        <header className="sticky top-0 z-30 w-full border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
            <div className="flex h-16 items-center gap-4 px-4 md:px-6">
                {/* Menu Button */}
                <Button
                    variant="ghost"
                    size="icon"
                    onClick={onMenuClick}
                    className="text-foreground"
                >
                    <Menu className="h-5 w-5" />
                </Button>

                {/* Title */}
                <div className="flex-1">
                    <h1 className="text-xl font-semibold text-foreground">
                        TEA Dashboard
                    </h1>
                    <p className="text-xs text-muted-foreground hidden sm:block">
                        Статистика диалогов Telegram-бота
                    </p>
                </div>

                {/* Controls */}
                <div className="flex items-center gap-2">
                    {/* Period Selector */}
                    <Select value={period} onValueChange={(value) => onPeriodChange(value as Period)}>
                        <SelectTrigger className="w-[140px] sm:w-[180px] text-foreground">
                            <SelectValue placeholder="Период" />
                        </SelectTrigger>
                        <SelectContent>
                            <SelectItem value="day">День</SelectItem>
                            <SelectItem value="week">Неделя</SelectItem>
                            <SelectItem value="month">Месяц</SelectItem>
                        </SelectContent>
                    </Select>

                    {/* Refresh Button */}
                    <Button
                        onClick={onRefresh}
                        variant="outline"
                        size="icon"
                        className="text-foreground"
                    >
                        <RefreshCw className="h-4 w-4" />
                    </Button>

                    {/* GitHub Button */}
                    <Button
                        asChild
                        variant="outline"
                        size="icon"
                        className="text-foreground"
                    >
                        <a
                            href="https://github.com/KaluginSysttech/TaskEstimatorAssistant"
                            target="_blank"
                            rel="noopener noreferrer"
                            aria-label="GitHub Repository"
                        >
                            <Github className="h-5 w-5" />
                        </a>
                    </Button>
                </div>
            </div>
        </header>
    );
}

