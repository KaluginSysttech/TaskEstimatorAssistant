"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Home, Settings, X } from "lucide-react";
import Link from "next/link";

interface AppSidebarProps {
    isOpen: boolean;
    onClose: () => void;
}

export function AppSidebar({ isOpen, onClose }: AppSidebarProps) {
    return (
        <>
            {/* Backdrop */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-40 lg:hidden"
                    onClick={onClose}
                />
            )}

            {/* Sidebar */}
            <aside
                className={cn(
                    "fixed left-0 top-0 z-50 h-screen w-64 bg-card border-r border-border transition-transform duration-300 ease-in-out",
                    isOpen ? "translate-x-0" : "-translate-x-full"
                )}
            >
                <div className="flex flex-col h-full">
                    {/* Header */}
                    <div className="flex items-center justify-between p-4 border-b border-border">
                        <div className="flex items-center gap-2">
                            <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                                <span className="text-primary-foreground font-bold text-lg">T</span>
                            </div>
                            <span className="font-semibold text-lg text-foreground">TEA Dashboard</span>
                        </div>
                        <Button
                            variant="ghost"
                            size="icon"
                            onClick={onClose}
                            className="lg:hidden"
                        >
                            <X className="h-5 w-5" />
                        </Button>
                    </div>

                    {/* Navigation */}
                    <nav className="flex-1 p-4 space-y-2">
                        <Link href="/" onClick={onClose}>
                            <Button
                                variant="ghost"
                                className="w-full justify-start gap-2 text-foreground hover:bg-accent"
                            >
                                <Home className="h-5 w-5" />
                                Dashboard
                            </Button>
                        </Link>
                        <Link href="/settings" onClick={onClose}>
                            <Button
                                variant="ghost"
                                className="w-full justify-start gap-2 text-muted-foreground hover:bg-accent"
                                disabled
                            >
                                <Settings className="h-5 w-5" />
                                Settings
                            </Button>
                        </Link>
                    </nav>

                    {/* Footer */}
                    <div className="p-4 border-t border-border">
                        <p className="text-xs text-muted-foreground">
                            Sprint S3: Dashboard UI
                        </p>
                    </div>
                </div>
            </aside>
        </>
    );
}

