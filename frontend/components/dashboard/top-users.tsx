"use client";

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
import type { TopUser } from "@/types/stats";
import { ChevronDown, ChevronUp } from "lucide-react";
import { useState } from "react";

interface TopUsersProps {
    users: TopUser[];
}

export function TopUsers({ users }: TopUsersProps) {
    const [isOpen, setIsOpen] = useState(false);

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleString("ru-RU", {
            day: "2-digit",
            month: "2-digit",
            year: "numeric",
        });
    };

    return (
        <Collapsible open={isOpen} onOpenChange={setIsOpen}>
            <Card className="border-border bg-card">
                <CardHeader>
                    <div className="flex items-center justify-between">
                        <div>
                            <CardTitle className="text-foreground">Топ пользователей</CardTitle>
                            <CardDescription className="text-muted-foreground">
                                {users.length} наиболее активных пользователей
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
                                    <TableHead className="text-muted-foreground w-16">#</TableHead>
                                    <TableHead className="text-muted-foreground">Пользователь</TableHead>
                                    <TableHead className="text-muted-foreground text-right">Диалогов</TableHead>
                                    <TableHead className="text-muted-foreground text-right">Сообщений</TableHead>
                                    <TableHead className="text-muted-foreground text-right">Последняя активность</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {users.map((user, index) => (
                                    <TableRow key={user.username}>
                                        <TableCell className="font-medium">
                                            <div className="flex items-center justify-center w-8 h-8 rounded-full bg-primary text-primary-foreground text-sm font-bold">
                                                {index + 1}
                                            </div>
                                        </TableCell>
                                        <TableCell className="font-medium text-foreground">
                                            {user.username}
                                        </TableCell>
                                        <TableCell className="text-right text-foreground">
                                            {user.conversation_count}
                                        </TableCell>
                                        <TableCell className="text-right text-foreground">
                                            {user.message_count}
                                        </TableCell>
                                        <TableCell className="text-right text-muted-foreground">
                                            {formatDate(user.last_active)}
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

