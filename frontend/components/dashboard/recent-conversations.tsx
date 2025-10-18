"use client";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import type { RecentConversation } from "@/types/stats";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface RecentConversationsProps {
    conversations: RecentConversation[];
}

export function RecentConversations({ conversations }: RecentConversationsProps) {
    const [isOpen, setIsOpen] = useState(false);

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleString("ru-RU", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
            hour: "2-digit",
            minute: "2-digit",
        });
    };

    return (
        <Collapsible open={isOpen} onOpenChange={setIsOpen}>
            <Card className="border-border bg-card">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle className="text-foreground">Последние диалоги</CardTitle>
                            <CardDescription className="text-muted-foreground">
                                {conversations.length} последних диалогов
                            </CardDescription>
                        </div>
                        <CollapsibleTrigger asChild>
                            <Button variant="outline" size="sm" className="text-foreground">
                                {isOpen ? (
                                    <>
                                        <ChevronUp className="h-4 w-4 mr-2" />
                                        Скрыть
                                    </>
                                ) : (
                                    <>
                                        <ChevronDown className="h-4 w-4 mr-2" />
                                        Показать
                                    </>
                                )}
                            </Button>
                        </CollapsibleTrigger>
                    </div>
                </CardHeader>
                <CollapsibleContent>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead className="text-muted-foreground">Пользователь</TableHead>
                                    <TableHead className="text-muted-foreground">Начало</TableHead>
                                    <TableHead className="text-muted-foreground text-right">Сообщений</TableHead>
                                    <TableHead className="text-muted-foreground text-right">Статус</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {conversations.map((conv) => (
                                    <TableRow key={conv.conversation_id}>
                                        <TableCell className="font-medium text-foreground">
                                            {conv.user_name}
                                        </TableCell>
                                        <TableCell className="text-muted-foreground">
                                            {formatDate(conv.started_at)}
                                        </TableCell>
                                        <TableCell className="text-right text-foreground">
                                            {conv.message_count}
                                        </TableCell>
                                        <TableCell className="text-right">
                                            <Badge
                                                variant={conv.status === "active" ? "default" : "secondary"}
                                            >
                                                {conv.status === "active" ? "Активен" : "Завершён"}
                                            </Badge>
                                        </TableCell>
                                    </TableRow>
                                ))}
                            </TableBody>
                        </Table>
                    </CardContent>
                </CollapsibleContent>
            </Card>
        </Collapsible>
    );
}

