#!/usr/bin/env python3
"""
Database Seeding Script for AEGIS Platform

This script:
1. Resets the database (drops and recreates all tables)
2. Creates 4 test user accounts (Faculty, Authority, Student, Admin)
3. Creates sample data for all 4 pillars

Usage:
    cd /home/apsingh/Documents/krkhc_2/backend
    source .venv/bin/activate
    python seed.py
"""

import asyncio
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import select
from app.db.database import engine, Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.grievance import (
    Grievance,
    GrievanceUpdate,
    GrievanceStatus,
    GrievanceCategory,
    Priority,
)
from app.models.academic import (
    Course,
    Enrollment,
    Resource,
    ResourceType,
    CalendarEvent,
)
from app.models.opportunity import (
    Opportunity,
    OpportunityType,
    Application,
    ApplicationStatus,
    Task,
    TaskStatus,
)

# Test account credentials
TEST_PASSWORD = "password123"
TEST_USERS = [
    # Faculty accounts (2)
    {
        "email": "faculty1@iitmandi.ac.in",
        "password": TEST_PASSWORD,
        "display_name": "Dr. Rajesh Kumar",
        "department": "Computer Science",
        "role": UserRole.FACULTY,
    },
    {
        "email": "faculty2@iitmandi.ac.in",
        "password": TEST_PASSWORD,
        "display_name": "Dr. Priya Sharma",
        "department": "Electrical Engineering",
        "role": UserRole.FACULTY,
    },
    # Authority accounts (2)
    {
        "email": "authority1@iitmandi.ac.in",
        "password": TEST_PASSWORD,
        "display_name": "Dr. Authority One",
        "department": "Computer Science",
        "role": UserRole.AUTHORITY,
    },
    {
        "email": "authority2@iitmandi.ac.in",
        "password": TEST_PASSWORD,
        "display_name": "Prof. Authority Two",
        "department": "Mechanical Engineering",
        "role": UserRole.AUTHORITY,
    },
    # Student accounts (2)
    {
        "email": "student1@students.iitmandi.ac.in",
        "password": TEST_PASSWORD,
        "display_name": "Rahul Verma",
        "department": "Computer Science",
        "role": UserRole.STUDENT,
    },
    {
        "email": "student2@students.iitmandi.ac.in",
        "password": TEST_PASSWORD,
        "display_name": "Neha Gupta",
        "department": "Electrical Engineering",
        "role": UserRole.STUDENT,
    },
    # Admin account (1)
    {
        "email": "admin@iitmandi.ac.in",
        "password": TEST_PASSWORD,
        "display_name": "System Admin",
        "department": "Computer Science",
        "role": UserRole.ADMIN,
    },
]


async def reset_database():
    """Drop all tables and recreate them."""
    print("🗑️  Resetting database...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database reset complete")


async def create_test_users():
    """Create test user accounts."""
    print("\n👥 Creating test users...")

    async for db in get_db():
        users = []
        for user_data in TEST_USERS:
            # Check if user already exists
            result = await db.execute(
                select(User).where(User.email == user_data["email"])
            )
            existing = result.scalar_one_or_none()

            if existing:
                print(f"  ⚠️  User {user_data['email']} already exists")
                users.append(existing)
                continue

            # Create user
            user = User(
                email=user_data["email"],
                password_hash=get_password_hash(user_data["password"]),
                display_name=user_data["display_name"],
                department=user_data["department"],
                role=user_data["role"],
                is_active=True,
            )
            db.add(user)
            await db.flush()  # Flush to get the ID
            users.append(user)
            print(f"  ✅ Created {user_data['role'].value}: {user_data['email']}")

        await db.commit()
        return users


async def create_sample_courses(users):
    """Create sample courses for multiple faculty."""
    print("\n📚 Creating sample courses...")

    async for db in get_db():
        # Get all faculty users
        faculties = [u for u in users if u.role == UserRole.FACULTY]
        if not faculties:
            print("  ⚠️  No faculty users found, skipping courses")
            return []

        courses_data = [
            {
                "code": "CS101",
                "name": "Introduction to Computer Science",
                "credits": 4,
                "semester": "Spring 2026",
                "department": "Computer Science",
                "description": "Fundamental concepts of computer science and programming. Topics include algorithms, data structures, and software engineering principles.",
                "professor_idx": 0,
            },
            {
                "code": "CS201",
                "name": "Data Structures and Algorithms",
                "credits": 4,
                "semester": "Spring 2026",
                "department": "Computer Science",
                "description": "Advanced data structures and algorithm design techniques. Arrays, linked lists, trees, graphs, sorting, and searching algorithms.",
                "professor_idx": 0,
            },
            {
                "code": "CS301",
                "name": "Machine Learning",
                "credits": 3,
                "semester": "Spring 2026",
                "department": "Computer Science",
                "description": "Introduction to machine learning algorithms, neural networks, deep learning, and practical applications.",
                "professor_idx": 0,
            },
            {
                "code": "EE101",
                "name": "Basic Electrical Engineering",
                "credits": 4,
                "semester": "Spring 2026",
                "department": "Electrical Engineering",
                "description": "Fundamentals of electrical engineering including circuits, signals, and systems.",
                "professor_idx": 1,
            },
            {
                "code": "EE201",
                "name": "Digital Signal Processing",
                "credits": 3,
                "semester": "Spring 2026",
                "department": "Electrical Engineering",
                "description": "Analysis and processing of digital signals, Fourier transforms, and filter design.",
                "professor_idx": 1,
            },
        ]

        courses = []
        for course_data in courses_data:
            professor_idx = course_data.pop("professor_idx")
            professor = faculties[professor_idx % len(faculties)]
            course = Course(professor_id=professor.id, **course_data)
            db.add(course)
            await db.flush()
            courses.append(course)
            print(
                f"  ✅ Created course: {course_data['code']} - {course_data['name']} (by {professor.display_name})"
            )

        await db.commit()
        return courses


async def create_sample_grievances(users):
    """Create sample grievances from multiple students."""
    print("\n🎫 Creating sample grievances...")

    async for db in get_db():
        students = [u for u in users if u.role == UserRole.STUDENT]
        if not students:
            print("  ⚠️  No student users found, skipping grievances")
            return []

        grievances_data = [
            {
                "title": "WiFi not working in Hostel Block A",
                "description": "The WiFi has been down for 3 days in Hostel Block A, rooms 101-150. Unable to attend online classes.",
                "category": GrievanceCategory.INFRASTRUCTURE,
                "priority": Priority.HIGH,
                "location": "Hostel Block A",
                "is_anonymous": False,
                "status": GrievanceStatus.SUBMITTED,
                "student_idx": 0,
            },
            {
                "title": "Library AC needs repair",
                "description": "The air conditioning in the main library reading room is not working properly. It's very hot during afternoon hours.",
                "category": GrievanceCategory.INFRASTRUCTURE,
                "priority": Priority.MEDIUM,
                "location": "Main Library",
                "is_anonymous": True,
                "status": GrievanceStatus.UNDER_REVIEW,
                "student_idx": 0,
            },
            {
                "title": "Canteen food quality issue",
                "description": "The quality of food in the main canteen has degraded significantly. Several students reported stomach issues.",
                "category": GrievanceCategory.FOOD,
                "priority": Priority.URGENT,
                "location": "Main Canteen",
                "is_anonymous": False,
                "status": GrievanceStatus.IN_PROGRESS,
                "student_idx": 1,
            },
            {
                "title": "Broken furniture in classroom B-204",
                "description": "Several chairs and desks in classroom B-204 are broken and need immediate replacement.",
                "category": GrievanceCategory.INFRASTRUCTURE,
                "priority": Priority.MEDIUM,
                "location": "Classroom B-204",
                "is_anonymous": False,
                "status": GrievanceStatus.SUBMITTED,
                "student_idx": 1,
            },
            {
                "title": "Hostel laundry machines not working",
                "description": "All three washing machines in Hostel Block C laundry room are out of order for the past week.",
                "category": GrievanceCategory.HOSTEL,
                "priority": Priority.HIGH,
                "location": "Hostel Block C Laundry",
                "is_anonymous": True,
                "status": GrievanceStatus.SUBMITTED,
                "student_idx": 0,
            },
        ]

        for grievance_data in grievances_data:
            student_idx = grievance_data.pop("student_idx")
            student = students[student_idx % len(students)]

            grievance = Grievance(
                submitter_id=student.id if not grievance_data["is_anonymous"] else None,
                **{k: v for k, v in grievance_data.items() if k != "status"},
            )
            grievance.status = grievance_data["status"]
            db.add(grievance)
            await db.flush()

            # Add initial update
            update = GrievanceUpdate(
                grievance_id=grievance.id,
                updated_by=student.id,
                status=grievance_data["status"],
                remark="Grievance submitted"
                if grievance_data["status"] == GrievanceStatus.SUBMITTED
                else "Under review by authority",
            )
            db.add(update)

            submitter_info = (
                student.display_name
                if not grievance_data["is_anonymous"]
                else "Anonymous"
            )
            print(
                f"  ✅ Created grievance: {grievance_data['title'][:50]}... (by {submitter_info})"
            )

        await db.commit()


async def create_sample_opportunities(users):
    """Create sample opportunities from multiple faculty and authority."""
    print("\n💼 Creating sample opportunities...")

    async for db in get_db():
        faculties = [u for u in users if u.role == UserRole.FACULTY]
        authorities = [u for u in users if u.role == UserRole.AUTHORITY]
        students = [u for u in users if u.role == UserRole.STUDENT]

        if not faculties or not authorities:
            print("  ⚠️  Faculty or Authority users not found, skipping opportunities")
            return

        opportunities_data = [
            {
                "title": "Research Assistant - Machine Learning",
                "description": "Looking for a motivated student to help with research on neural networks and deep learning applications in computer vision.",
                "type": OpportunityType.RESEARCH,
                "skills": ["Python", "Machine Learning", "TensorFlow", "PyTorch"],
                "duration": "6 months",
                "stipend": "8000/month",
                "deadline": datetime.now() + timedelta(days=30),
                "is_open": True,
                "creator_idx": 0,  # faculty1
                "creator_type": "faculty",
            },
            {
                "title": "Summer Internship - Web Development",
                "description": "Full-stack web development internship. Work on real projects using React, Node.js, and PostgreSQL.",
                "type": OpportunityType.INTERNSHIP,
                "skills": ["JavaScript", "React", "Node.js", "PostgreSQL"],
                "duration": "3 months",
                "stipend": "15000/month",
                "deadline": datetime.now() + timedelta(days=45),
                "is_open": True,
                "creator_idx": 0,  # faculty1
                "creator_type": "faculty",
            },
            {
                "title": "Research Project - Data Science",
                "description": "Authority-sponsored research project on campus data analytics and student performance prediction.",
                "type": OpportunityType.RESEARCH,
                "skills": ["Python", "Data Science", "Statistics", "Pandas"],
                "duration": "1 year",
                "stipend": "10000/month",
                "deadline": datetime.now() + timedelta(days=60),
                "is_open": True,
                "creator_idx": 0,  # authority1
                "creator_type": "authority",
            },
            {
                "title": "Research Assistant - IoT Systems",
                "description": "Work on Internet of Things research projects involving sensors, embedded systems, and data collection.",
                "type": OpportunityType.RESEARCH,
                "skills": ["C++", "Arduino", "Raspberry Pi", "Embedded Systems"],
                "duration": "6 months",
                "stipend": "9000/month",
                "deadline": datetime.now() + timedelta(days=35),
                "is_open": True,
                "creator_idx": 1,  # faculty2
                "creator_type": "faculty",
            },
            {
                "title": "Campus Sustainability Project",
                "description": "Lead research on campus sustainability initiatives and green energy solutions.",
                "type": OpportunityType.RESEARCH,
                "skills": ["Research", "Data Analysis", "Sustainability", "Reporting"],
                "duration": "8 months",
                "stipend": "7500/month",
                "deadline": datetime.now() + timedelta(days=50),
                "is_open": True,
                "creator_idx": 1,  # authority2
                "creator_type": "authority",
            },
        ]

        for opp_data in opportunities_data:
            creator_idx = opp_data.pop("creator_idx")
            creator_type = opp_data.pop("creator_type")

            if creator_type == "faculty":
                creator = faculties[creator_idx % len(faculties)]
            else:
                creator = authorities[creator_idx % len(authorities)]

            opportunity = Opportunity(faculty_id=creator.id, **opp_data)
            db.add(opportunity)
            await db.flush()
            print(
                f"  ✅ Created opportunity: {opp_data['title']} (by {creator.display_name})"
            )

            # Create sample applications from both students
            for i, student in enumerate(students):
                application = Application(
                    opportunity_id=opportunity.id,
                    student_id=student.id,
                    status=ApplicationStatus.SUBMITTED
                    if i == 0
                    else ApplicationStatus.UNDER_REVIEW,
                    cover_letter=f"I am very interested in this {opp_data['type'].value.lower()} position. I have relevant experience in {', '.join(opp_data['skills'][:2])} and am eager to contribute.",
                )
                db.add(application)
                print(f"    📝 Created application from {student.display_name}")

        await db.commit()


async def create_sample_tasks(users):
    """Create sample tasks for multiple students."""
    print("\n✅ Creating sample tasks...")

    async for db in get_db():
        students = [u for u in users if u.role == UserRole.STUDENT]
        if not students:
            print("  ⚠️  No student users found, skipping tasks")
            return

        # Tasks for student1 (Rahul)
        tasks_student1 = [
            {
                "title": "Complete ML Assignment",
                "description": "Finish the neural network assignment for CS301",
                "category": "Academic",
                "status": TaskStatus.IN_PROGRESS,
                "progress": 60,
            },
            {
                "title": "Prepare for Midterm",
                "description": "Study chapters 1-5 for CS201 midterm exam",
                "category": "Academic",
                "status": TaskStatus.PENDING,
                "progress": 0,
            },
            {
                "title": "Research Paper Reading",
                "description": "Read and summarize 3 papers on deep learning",
                "category": "Research",
                "status": TaskStatus.COMPLETED,
                "progress": 100,
            },
        ]

        # Tasks for student2 (Neha)
        tasks_student2 = [
            {
                "title": "Complete Circuit Design Lab",
                "description": "Design and simulate amplifier circuit for EE lab",
                "category": "Academic",
                "status": TaskStatus.IN_PROGRESS,
                "progress": 40,
            },
            {
                "title": "Signal Processing Project",
                "description": "Implement FFT algorithm for DSP course",
                "category": "Academic",
                "status": TaskStatus.PENDING,
                "progress": 10,
            },
            {
                "title": "Apply for Summer Internship",
                "description": "Prepare resume and apply to 5 companies",
                "category": "Career",
                "status": TaskStatus.IN_PROGRESS,
                "progress": 75,
            },
            {
                "title": "Gym Workout",
                "description": "Daily workout routine - cardio and weights",
                "category": "Personal",
                "status": TaskStatus.PENDING,
                "progress": 0,
            },
        ]

        all_tasks = [(students[0], tasks_student1), (students[1], tasks_student2)]

        for student, tasks_data in all_tasks:
            for task_data in tasks_data:
                task = Task(student_id=student.id, **task_data)
                db.add(task)
                print(
                    f"  ✅ Created task: {task_data['title']} (for {student.display_name})"
                )

        await db.commit()


async def seed_database():
    """Main seeding function."""
    print("=" * 60)
    print("🌱 AEGIS Platform - Database Seeding Script")
    print("=" * 60)

    try:
        # Reset database
        await reset_database()

        # Create test users
        users = await create_test_users()

        # Create sample data
        await create_sample_courses(users)
        await create_sample_grievances(users)
        await create_sample_opportunities(users)
        await create_sample_tasks(users)

        print("\n" + "=" * 60)
        print("✅ Seeding completed successfully!")
        print("=" * 60)
        print("\n📋 Test Accounts Created:")
        print("-" * 60)
        for user in TEST_USERS:
            print(
                f"  Role: {user['role'].value:10} | Email: {user['email']:<35} | Password: {user['password']}"
            )
        print("-" * 60)
        print("\n🚀 You can now login with any of these accounts!")
        print("   API: http://localhost:8000")
        print("   Frontend: http://localhost:3000")
        print("\n📝 Next steps:")
        print("   1. Start backend: cd backend && ./start.sh")
        print("   2. Start frontend: cd frontend && npm run dev")
        print("   3. Login with test accounts and explore!")

    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(seed_database())
