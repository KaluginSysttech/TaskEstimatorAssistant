"use client";

import type { Period } from "@/types/stats";
import { useEffect, useState } from "react";
import { AppHeader } from "./app-header";
import { AppSidebar } from "./app-sidebar";

interface DashboardLayoutProps {
    children: React.ReactNode;
    period: Period;
    onPeriodChange: (period: Period) => void;
    onRefresh: () => void;
}

export function DashboardLayout({
    children,
    period,
    onPeriodChange,
    onRefresh,
}: DashboardLayoutProps) {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [mounted, setMounted] = useState(false);

    // Load sidebar state from localStorage only after mount (client-side only)
    useEffect(() => {
        setMounted(true);
        const saved = localStorage.getItem("sidebar-open");
        if (saved !== null) {
            setSidebarOpen(saved === "true");
        }
    }, []);

    // Save sidebar state to localStorage (only after mounted to avoid hydration issues)
    useEffect(() => {
        if (mounted) {
            localStorage.setItem("sidebar-open", String(sidebarOpen));
        }
    }, [sidebarOpen, mounted]);

    return (
        <div className="min-h-screen bg-background">
            <AppSidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
            />
            <div className="flex flex-col min-h-screen">
                <AppHeader
                    period={period}
                    onPeriodChange={onPeriodChange}
                    onRefresh={onRefresh}
                    onMenuClick={() => setSidebarOpen(!sidebarOpen)}
                />
                <main className="flex-1">
                    {children}
                </main>
            </div>
        </div>
    );
}

