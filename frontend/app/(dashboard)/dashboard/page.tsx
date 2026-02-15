"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useAuthStore } from "@/stores/auth";
import { grievancesApi, coursesApi, opportunitiesApi } from "@/lib/api";
import { toast } from "sonner";

export default function DashboardPage() {
  const { user } = useAuthStore();
  const [stats, setStats] = useState({
    grievances: 0,
    courses: 0,
    applications: 0,
    tasks: 0
  });
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const [
          grievances,
          enrollments,
          applications,
          tasks
        ] = await Promise.all([
          grievancesApi.list({ status: "SUBMITTED" }), // customized later
          coursesApi.getMyEnrollments(),
          opportunitiesApi.getMyApplications(),
          opportunitiesApi.getMyTasks({ status: "PENDING" })
        ]);

        // Filter active grievances if needed, for now just count all the user's active ones
        // The list API for students already filters to their own.
        // We might want to filter by status != RESOLVED for "active" count
        const activeGrievances = grievances.filter((g: any) => g.status !== "RESOLVED");

        setStats({
          grievances: activeGrievances.length,
          courses: enrollments.length,
          applications: applications.length,
          tasks: tasks.length
        });
      } catch (error) {
        console.error("Failed to load dashboard stats", error);
        // Don't show toast on dashboard to avoid annoyance, just log
      } finally {
        setIsLoading(false);
      }
    }

    if (user) {
      loadStats();
    }
  }, [user]);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">
          Welcome back, {user?.display_name || "User"}
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Grievances</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.grievances}</div>
            <p className="text-xs text-muted-foreground">
              {stats.grievances === 0 ? "No active grievances" : "Pending resolution"}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Enrolled Courses</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.courses}</div>
            <p className="text-xs text-muted-foreground">
              {stats.courses === 0 ? "No enrolled courses" : "Active enrollments"}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Applications</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.applications}</div>
            <p className="text-xs text-muted-foreground">
              {stats.applications === 0 ? "No pending applications" : "Pending review"}
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pending Tasks</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.tasks}</div>
            <p className="text-xs text-muted-foreground">
              {stats.tasks === 0 ? "No pending tasks" : "Due soon"}
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <a
              href="/grievances/new"
              className="block p-4 bg-blue-50 hover:bg-blue-100 rounded-lg transition-colors"
            >
              <h3 className="font-semibold text-blue-900">Submit Grievance</h3>
              <p className="text-sm text-blue-700">
                Report an issue or concern
              </p>
            </a>
            <a
              href="/opportunities"
              className="block p-4 bg-green-50 hover:bg-green-100 rounded-lg transition-colors"
            >
              <h3 className="font-semibold text-green-900">Browse Opportunities</h3>
              <p className="text-sm text-green-700">
                Find internships and research positions
              </p>
            </a>
            <a
              href="/courses"
              className="block p-4 bg-purple-50 hover:bg-purple-100 rounded-lg transition-colors"
            >
              <h3 className="font-semibold text-purple-900">View Courses</h3>
              <p className="text-sm text-purple-700">
                Access study materials and resources
              </p>
            </a>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Recent Activity</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-gray-500 text-center py-8">
              No recent activity to display
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}