"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Clock, MapPin, User } from "lucide-react";
import Link from "next/link";

// Mock data - replace with API call
const mockGrievance = {
  id: "1",
  title: "Water leakage in Hostel Block A",
  category: "INFRASTRUCTURE",
  priority: "HIGH",
  location: "Hostel Block A, Room 203",
  description:
    "There has been a water leakage from the ceiling in my room for the past 3 days. It's getting worse and water is accumulating on the floor. This needs immediate attention.",
  status: "IN_PROGRESS",
  isAnonymous: false,
  submitterName: "John Doe",
  createdAt: "2026-02-14T10:30:00Z",
  updatedAt: "2026-02-14T14:20:00Z",
  photos: [],
  updates: [
    {
      id: "1",
      status: "SUBMITTED",
      remark: "Grievance submitted successfully",
      createdAt: "2026-02-14T10:30:00Z",
      updatedBy: "System",
    },
    {
      id: "2",
      status: "UNDER_REVIEW",
      remark: "Maintenance team has been notified and will inspect today",
      createdAt: "2026-02-14T12:00:00Z",
      updatedBy: "Hostel Authority",
    },
    {
      id: "3",
      status: "IN_PROGRESS",
      remark: "Plumber assigned. Work will begin tomorrow morning.",
      createdAt: "2026-02-14T14:20:00Z",
      updatedBy: "Maintenance Department",
    },
  ],
};

const statusColors: Record<string, string> = {
  SUBMITTED: "bg-yellow-100 text-yellow-800",
  UNDER_REVIEW: "bg-blue-100 text-blue-800",
  IN_PROGRESS: "bg-purple-100 text-purple-800",
  RESOLVED: "bg-green-100 text-green-800",
};

const priorityColors: Record<string, string> = {
  LOW: "bg-gray-100 text-gray-800",
  MEDIUM: "bg-yellow-100 text-yellow-800",
  HIGH: "bg-orange-100 text-orange-800",
  URGENT: "bg-red-100 text-red-800",
};

export default function GrievanceDetailPage({ params }: { params: { id: string } }) {
  const [grievance] = useState(mockGrievance);

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <Link
          href="/grievances"
          className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="w-4 h-4 mr-1" />
          Back to Grievances
        </Link>
      </div>

      <div className="space-y-6">
        {/* Main Grievance Card */}
        <Card>
          <CardHeader className="border-b">
            <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
              <div className="flex-1">
                <div className="flex flex-wrap items-center gap-2 mb-2">
                  <Badge className={statusColors[grievance.status]}>
                    {grievance.status.replace("_", " ")}
                  </Badge>
                  <Badge className={priorityColors[grievance.priority]}>
                    {grievance.priority} Priority
                  </Badge>
                </div>
                <CardTitle className="text-xl">{grievance.title}</CardTitle>
              </div>
              <div className="text-sm text-gray-500">
                <span>ID: {grievance.id}</span>
              </div>
            </div>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Meta Info */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-sm">
              <div className="flex items-center gap-2 text-gray-600">
                <User className="w-4 h-4" />
                <span>
                  {grievance.isAnonymous ? "Anonymous" : grievance.submitterName}
                </span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <MapPin className="w-4 h-4" />
                <span>{grievance.location}</span>
              </div>
              <div className="flex items-center gap-2 text-gray-600">
                <Clock className="w-4 h-4" />
                <span>{new Date(grievance.createdAt).toLocaleDateString()}</span>
              </div>
            </div>

            {/* Description */}
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Description</h3>
              <p className="text-gray-600">{grievance.description}</p>
            </div>

            {/* Category */}
            <div>
              <h3 className="font-medium text-gray-900 mb-2">Category</h3>
              <Badge variant="outline">{grievance.category}</Badge>
            </div>
          </CardContent>
        </Card>

        {/* Timeline */}
        <Card>
          <CardHeader>
            <CardTitle>Status Timeline</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {grievance.updates.map((update, index) => (
                <div key={update.id} className="flex gap-4">
                  <div className="flex flex-col items-center">
                    <div
                      className={`w-3 h-3 rounded-full ${
                        index === 0 ? "bg-gray-300" : "bg-blue-500"
                      }`}
                    />
                    {index < grievance.updates.length - 1 && (
                      <div className="w-0.5 h-full bg-gray-200 mt-2" />
                    )}
                  </div>
                  <div className="flex-1 pb-6">
                    <div className="flex flex-col sm:flex-row sm:items-center gap-1 sm:gap-4 mb-1">
                      <Badge className={statusColors[update.status]}>
                        {update.status.replace("_", " ")}
                      </Badge>
                      <span className="text-sm text-gray-500">
                        {new Date(update.createdAt).toLocaleString()}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 mb-1">{update.remark}</p>
                    <p className="text-xs text-gray-400">by {update.updatedBy}</p>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}