"use client";

import { useState, useEffect, use } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { ArrowLeft, Users, FileText } from "lucide-react";
import Link from "next/link";
import { coursesApi } from "@/lib/api";
import { toast } from "sonner";

interface Course {
  id: string;
  code: string;
  name: string;
  credits: number;
  department: string;
  description: string | null;
  professor_id: string | null;
  professor_name: string | null;
  enrollment_count: number;
  semester: string;
}

export default function CourseDetailPage({ params }: { params: Promise<{ id: string }> }) {
  // Unwrap params using React.use()
  const { id: courseId } = use(params);
  
  const [course, setCourse] = useState<Course | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isEnrolling, setIsEnrolling] = useState(false);

  useEffect(() => {
    loadCourse();
  }, [courseId]);

  const loadCourse = async () => {
    try {
      setIsLoading(true);
      setError(null);
      const data = await coursesApi.get(courseId);
      setCourse(data);
    } catch (err: any) {
      if (err.response?.status === 403) {
        setError("You must be enrolled in this course to view details.");
      } else {
        setError("Failed to load course. Please try again.");
        toast.error("Failed to load course");
      }
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEnroll = async () => {
    try {
      setIsEnrolling(true);
      await coursesApi.enroll(courseId);
      toast.success("Successfully enrolled!");
      // Reload to show course content
      loadCourse();
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Failed to enroll");
      console.error(err);
    } finally {
      setIsEnrolling(false);
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center">
        <p className="text-gray-500">Loading course...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="mb-6">
          <Link
            href="/courses"
            className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="w-4 h-4 mr-1" />
            Back to Courses
          </Link>
        </div>

        <Card className="p-8 text-center">
          <CardContent>
            <p className="text-gray-500 mb-4">{error}</p>
            <Button onClick={handleEnroll} disabled={isEnrolling}>
              {isEnrolling ? "Enrolling..." : "Enroll Now"}
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  if (!course) {
    return (
      <div className="max-w-4xl mx-auto p-8 text-center">
        <p className="text-gray-500">Course not found</p>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-6">
        <Link
          href="/courses"
          className="inline-flex items-center text-sm text-gray-600 hover:text-gray-900"
        >
          <ArrowLeft className="w-4 h-4 mr-1" />
          Back to Courses
        </Link>
      </div>

      {/* Course Header */}
      <Card className="mb-6">
        <CardHeader>
          <div className="flex flex-col sm:flex-row sm:items-start sm:justify-between gap-4">
            <div>
              <div className="flex items-center gap-2 mb-2">
                <Badge variant="secondary">{course.code}</Badge>
                <Badge>{course.credits} Credits</Badge>
              </div>
              <CardTitle className="text-2xl">{course.name}</CardTitle>
              <p className="text-gray-500 mt-1">{course.department}</p>
            </div>
          </div>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-gray-600">{course.description || "No description available"}</p>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-4 border-t">
            <div>
              <p className="text-sm text-gray-500">Professor</p>
              <p className="font-medium">{course.professor_name || "TBA"}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Semester</p>
              <p className="font-medium">{course.semester}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Enrolled Students</p>
              <div className="flex items-center gap-2">
                <Users className="w-4 h-4 text-gray-400" />
                <span className="font-medium">{course.enrollment_count}</span>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Tabs */}
      <Tabs defaultValue="resources" className="space-y-6">
        <TabsList className="grid w-full grid-cols-3 lg:w-[400px]">
          <TabsTrigger value="resources">Resources</TabsTrigger>
          <TabsTrigger value="assignments">Assignments</TabsTrigger>
          <TabsTrigger value="grades">Grades</TabsTrigger>
        </TabsList>

        <TabsContent value="resources" className="space-y-4">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <FileText className="w-5 h-5" />
                Study Materials
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="p-8 text-center text-gray-500">
                <p>Resources will be available here.</p>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="assignments">
          <Card>
            <CardContent className="p-8 text-center text-gray-500">
              <p>No assignments available yet.</p>
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="grades">
          <Card>
            <CardContent className="p-8 text-center text-gray-500">
              <p>Grades will be available here.</p>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
}
