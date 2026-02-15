"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Calendar as CalendarIcon } from "lucide-react";

export default function CalendarPage() {
    return (
        <div className="space-y-6">
            <div>
                <h1 className="text-2xl font-bold text-gray-900">Calendar</h1>
                <p className="text-gray-600 mt-1">
                    View your academic schedule and upcoming events
                </p>
            </div>

            <Card className="min-h-[400px] flex flex-col items-center justify-center text-center p-8">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
                    <CalendarIcon className="w-8 h-8 text-blue-600" />
                </div>
                <CardTitle className="text-xl mb-2">Coming Soon</CardTitle>
                <p className="text-gray-500 max-w-md">
                    The calendar feature is currently under development. Soon you will be able to view your class schedule, exam dates, and improved event tracking here.
                </p>
            </Card>
        </div>
    );
}
