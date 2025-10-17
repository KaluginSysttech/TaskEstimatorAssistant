"use client";

/**
 * Главная страница - Dashboard статистики TEA бота
 * Sprint S3: Полноценный UI с графиками и таблицами
 */

import { ActivityChartComponent } from "@/components/dashboard/activity-chart";
import { RecentConversations } from "@/components/dashboard/recent-conversations";
import { StatCards } from "@/components/dashboard/stat-cards";
import { TopUsers } from "@/components/dashboard/top-users";
import { DashboardLayout } from "@/components/layout/dashboard-layout";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useStats } from "@/hooks/use-stats";
import type { Period } from "@/types/stats";
import { useState } from "react";

export default function DashboardPage() {
  const [period, setPeriod] = useState<Period>("week");
  const { data, loading, error, refetch } = useStats(period);

  // Обработчик изменения периода
  const handlePeriodChange = (period: Period) => {
    setPeriod(period);
  };

  return (
    <DashboardLayout
      period={period}
      onPeriodChange={handlePeriodChange}
      onRefresh={refetch}
    >
      <div className="container mx-auto p-4 md:p-6 lg:p-8 space-y-6">
        {/* Loading State */}
        {loading && (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-muted-foreground">Загрузка данных...</p>
            </div>
          </div>
        )}

        {/* Error State */}
        {error && (
          <Card className="border-destructive">
            <CardHeader>
              <CardTitle className="text-destructive">Ошибка загрузки</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-foreground mb-4">{error}</p>
              <Button onClick={refetch} variant="outline">
                Попробовать снова
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Success State - Полноценный дашборд */}
        {!loading && !error && data && (
          <div className="space-y-6">
            {/* KPI Cards */}
            <StatCards summary={data.summary} />

            {/* Activity Chart */}
            <ActivityChartComponent
              activityChart={data.activity_chart}
              period={period}
            />

            {/* Recent Conversations & Top Users */}
            <div className="grid gap-6 lg:grid-cols-2">
              <RecentConversations conversations={data.recent_conversations} />
              <TopUsers users={data.top_users} />
            </div>
          </div>
        )}

        {/* Footer */}
        <div className="text-center text-sm text-muted-foreground pt-8 border-t border-border">
          <p className="text-foreground font-medium">TEA Dashboard • Sprint S3: Dashboard UI</p>
          <p className="mt-1">
            Mock API на{" "}
            <code className="bg-muted px-2 py-1 rounded text-xs text-foreground">
              http://localhost:8001
            </code>
          </p>
        </div>
      </div>
    </DashboardLayout>
  );
}
