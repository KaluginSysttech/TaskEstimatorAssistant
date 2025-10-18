import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import type { Summary } from "@/types/stats";
import { ArrowDown, ArrowUp, Minus } from "lucide-react";

interface StatCardsProps {
    summary: Summary;
}

export function StatCards({ summary }: StatCardsProps) {
    const cards = [
        {
            title: "Всего диалогов",
            value: Math.round(summary.total_conversations.value),
            metric: summary.total_conversations,
        },
        {
            title: "Активные пользователи",
            value: Math.round(summary.active_users.value),
            metric: summary.active_users,
        },
        {
            title: "Средняя длина диалога",
            value: summary.avg_conversation_length.value.toFixed(1),
            metric: summary.avg_conversation_length,
        },
        {
            title: "Скорость роста",
            value: `${summary.growth_rate.value.toFixed(1)}%`,
            metric: summary.growth_rate,
        },
    ];

    const getTrendIcon = (trend: string) => {
        switch (trend) {
            case "up":
                return <ArrowUp className="h-3 w-3" />;
            case "down":
                return <ArrowDown className="h-3 w-3" />;
            default:
                return <Minus className="h-3 w-3" />;
        }
    };

    const getTrendVariant = (trend: string) => {
        switch (trend) {
            case "up":
                return "default";
            case "down":
                return "destructive";
            default:
                return "secondary";
        }
    };

    return (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {cards.map((card) => (
                <Card key={card.title} className="border-border bg-card">
                    <CardHeader className="pb-2">
                        <CardDescription className="text-muted-foreground">
                            {card.title}
                        </CardDescription>
                        <CardTitle className="text-3xl font-bold text-foreground">
                            {card.value}
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="flex items-center gap-2">
                            <Badge
                                variant={getTrendVariant(card.metric.trend)}
                                className="flex items-center gap-1"
                            >
                                {getTrendIcon(card.metric.trend)}
                                {card.metric.change_percent > 0 ? "+" : ""}
                                {card.metric.change_percent.toFixed(1)}%
                            </Badge>
                        </div>
                        <p className="text-xs text-muted-foreground mt-2">
                            {card.metric.description}
                        </p>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}

