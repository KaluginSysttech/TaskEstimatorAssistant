"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs";
import type { ActivityChart } from "@/types/stats";
import { Area, AreaChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

interface ActivityChartComponentProps {
    activityChart: ActivityChart;
    period: string;
}

export function ActivityChartComponent({ activityChart, period }: ActivityChartComponentProps) {
    // Transform data for recharts
    const chartData = activityChart.labels.map((label, index) => ({
        name: label,
        value: activityChart.values[index],
    }));

    const getDescription = (period: string) => {
        switch (period) {
            case "day":
                return "Активность по часам за последние 24 часа";
            case "week":
                return "Активность по дням за последнюю неделю";
            case "month":
                return "Активность по дням за последний месяц";
            default:
                return "График активности";
        }
    };

    return (
        <Card className="border-border bg-card">
            <CardHeader>
                <div className="flex items-center justify-between">
                    <div>
                        <CardTitle className="text-foreground">График активности</CardTitle>
                        <CardDescription className="text-muted-foreground">
                            {getDescription(period)}
                        </CardDescription>
                    </div>
                    <Tabs defaultValue={period} className="hidden">
                        <TabsList>
                            <TabsTrigger value="day">7 дней</TabsTrigger>
                            <TabsTrigger value="week">30 дней</TabsTrigger>
                            <TabsTrigger value="month">3 месяца</TabsTrigger>
                        </TabsList>
                    </Tabs>
                </div>
            </CardHeader>
            <CardContent>
                <div className="h-[300px] w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart
                            data={chartData}
                            margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
                        >
                            <defs>
                                <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.8} />
                                    <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0.1} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid
                                strokeDasharray="3 3"
                                stroke="hsl(var(--border))"
                                opacity={0.3}
                            />
                            <XAxis
                                dataKey="name"
                                stroke="hsl(var(--muted-foreground))"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                            />
                            <YAxis
                                stroke="hsl(var(--muted-foreground))"
                                fontSize={12}
                                tickLine={false}
                                axisLine={false}
                                tickFormatter={(value) => `${value}`}
                            />
                            <Tooltip
                                contentStyle={{
                                    backgroundColor: "hsl(var(--popover))",
                                    border: "1px solid hsl(var(--border))",
                                    borderRadius: "8px",
                                    color: "hsl(var(--popover-foreground))",
                                }}
                                labelStyle={{ color: "hsl(var(--foreground))" }}
                            />
                            <Area
                                type="monotone"
                                dataKey="value"
                                stroke="hsl(var(--primary))"
                                strokeWidth={2}
                                fillOpacity={1}
                                fill="url(#colorValue)"
                            />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </CardContent>
        </Card>
    );
}

