"use client";

/**
 * Главная страница - Dashboard статистики TEA бота
 */

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { useStats } from "@/hooks/use-stats";
import type { Period } from "@/types/stats";
import { useState } from "react";

export default function DashboardPage() {
  const [period, setPeriod] = useState<Period>("week");
  const { data, loading, error, refetch } = useStats(period);

  // Обработчик изменения периода
  const handlePeriodChange = (value: string) => {
    setPeriod(value as Period);
  };

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="max-w-7xl mx-auto space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-4xl font-bold tracking-tight">
              TEA Dashboard
            </h1>
            <p className="text-muted-foreground mt-2">
              Статистика диалогов Telegram-бота
            </p>
          </div>

          <div className="flex items-center gap-4">
            <Select value={period} onValueChange={handlePeriodChange}>
              <SelectTrigger className="w-[180px]">
                <SelectValue placeholder="Выберите период" />
              </SelectTrigger>
              <SelectContent>
                <SelectItem value="day">День (24 часа)</SelectItem>
                <SelectItem value="week">Неделя (7 дней)</SelectItem>
                <SelectItem value="month">Месяц (30 дней)</SelectItem>
              </SelectContent>
            </Select>

            <Button onClick={refetch} variant="outline" size="sm">
              Обновить
            </Button>
          </div>
        </div>

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <p className="text-muted-foreground">Загрузка данных...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="border-destructive">
            <CardHeader>
              <CardTitle className="text-destructive">Ошибка загрузки</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">{error}</p>
              <Button onClick={refetch} variant="outline" className="mt-4">
                Попробовать снова
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Success State - Минимальный дашборд */}
        {!loading && !error && data && (
          <div className="space-y-8">
            {/* KPI Cards */}
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
              <Card>
                <CardHeader className="pb-2">
                  <CardDescription>Всего диалогов</CardDescription>
                  <CardTitle className="text-3xl">
                    {Math.round(data.summary.total_conversations.value)}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Badge
                    variant={
                      data.summary.total_conversations.trend === "up"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {data.summary.total_conversations.change_percent > 0 ? "+" : ""}
                    {data.summary.total_conversations.change_percent.toFixed(1)}%
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-2">
                    {data.summary.total_conversations.description}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardDescription>Активные пользователи</CardDescription>
                  <CardTitle className="text-3xl">
                    {Math.round(data.summary.active_users.value)}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Badge
                    variant={
                      data.summary.active_users.trend === "up"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {data.summary.active_users.change_percent > 0 ? "+" : ""}
                    {data.summary.active_users.change_percent.toFixed(1)}%
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-2">
                    {data.summary.active_users.description}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardDescription>Средняя длина диалога</CardDescription>
                  <CardTitle className="text-3xl">
                    {data.summary.avg_conversation_length.value.toFixed(1)}
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Badge
                    variant={
                      data.summary.avg_conversation_length.trend === "up"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {data.summary.avg_conversation_length.change_percent > 0 ? "+" : ""}
                    {data.summary.avg_conversation_length.change_percent.toFixed(1)}%
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-2">
                    {data.summary.avg_conversation_length.description}
                  </p>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="pb-2">
                  <CardDescription>Скорость роста</CardDescription>
                  <CardTitle className="text-3xl">
                    {data.summary.growth_rate.value.toFixed(1)}%
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <Badge
                    variant={
                      data.summary.growth_rate.trend === "up"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {data.summary.growth_rate.change_percent > 0 ? "+" : ""}
                    {data.summary.growth_rate.change_percent.toFixed(1)}%
                  </Badge>
                  <p className="text-xs text-muted-foreground mt-2">
                    {data.summary.growth_rate.description}
                  </p>
                </CardContent>
              </Card>
            </div>

            {/* Activity Chart Placeholder */}
            <Card>
              <CardHeader>
                <CardTitle>График активности</CardTitle>
                <CardDescription>
                  {period === "day" && "Активность по часам за последние 24 часа"}
                  {period === "week" && "Активность по дням за последнюю неделю"}
                  {period === "month" && "Активность по дням за последний месяц"}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-[200px] flex items-center justify-center bg-muted rounded-md">
                  <p className="text-muted-foreground text-sm">
                    График будет реализован в Sprint F3
                  </p>
                </div>
              </CardContent>
            </Card>

            {/* Recent Conversations & Top Users Grid */}
            <div className="grid gap-4 md:grid-cols-2">
              {/* Recent Conversations Placeholder */}
              <Card>
                <CardHeader>
                  <CardTitle>Последние диалоги</CardTitle>
                  <CardDescription>
                    {data.recent_conversations.length} последних диалогов
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {data.recent_conversations.slice(0, 5).map((conv) => (
                      <div
                        key={conv.conversation_id}
                        className="flex items-center justify-between p-2 rounded-md hover:bg-muted"
                      >
                        <div>
                          <p className="text-sm font-medium">{conv.user_name}</p>
                          <p className="text-xs text-muted-foreground">
                            {conv.message_count} сообщений
                          </p>
                        </div>
                        <Badge variant={conv.status === "active" ? "default" : "secondary"}>
                          {conv.status}
                        </Badge>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>

              {/* Top Users Placeholder */}
              <Card>
                <CardHeader>
                  <CardTitle>Топ пользователей</CardTitle>
                  <CardDescription>
                    {data.top_users.length} наиболее активных пользователей
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    {data.top_users.map((user, index) => (
                      <div
                        key={user.username}
                        className="flex items-center justify-between p-2 rounded-md hover:bg-muted"
                      >
                        <div className="flex items-center gap-3">
                          <div className="flex items-center justify-center w-6 h-6 rounded-full bg-primary text-primary-foreground text-xs font-bold">
                            {index + 1}
                          </div>
                          <div>
                            <p className="text-sm font-medium">{user.username}</p>
                            <p className="text-xs text-muted-foreground">
                              {user.conversation_count} диалогов
                            </p>
                          </div>
                        </div>
                        <p className="text-sm text-muted-foreground">
                          {user.message_count} сообщений
                        </p>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center text-sm text-muted-foreground pt-8 border-t">
          <p>TEA Dashboard • Sprint F2: Frontend Initialization</p>
          <p className="mt-1">
            Mock API на{" "}
            <code className="bg-muted px-1 py-0.5 rounded text-xs">
              http://localhost:8001
            </code>
          </p>
        </div>
      </div>
    </div>
  );
}
