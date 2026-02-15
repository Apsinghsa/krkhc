# AEGIS Platform - Project Status & Handover Document

**Created**: February 14, 2026  
**Last Updated**: February 15, 2026  
**Status**: ✅ **PRODUCTION DEPLOYED** - All 4 Core Pillars Live

## 🌐 Production URLs

- **Frontend**: https://aegis-protocol-krkhc.vercel.app
- **Backend**: https://krkhc-production.up.railway.app
- **API Docs**: https://krkhc-production.up.railway.app/docs

---

## 📋 Project Overview

**AEGIS (Academic & Governance Integrated System)** - A unified web platform for IIT Mandi that brings together students, faculty, and administration.

**Architecture**: Decoupled monorepo
- Frontend: Next.js 16 + TypeScript + Tailwind + shadcn/ui
- Backend: FastAPI + SQLAlchemy + PostgreSQL + Redis
- Database: PostgreSQL (Docker)
- Auth: JWT-based with role-based access control

**Tech Stack from DOCX**:
- Frontend: Next.js 16, TypeScript, TanStack Query, Zustand, RHF, Zod, shadcn/ui
- Backend: FastAPI, SQLAlchemy 2.0, asyncpg, JWT, Redis
- Database: Local PostgreSQL in Docker
- File Storage: Local (can be upgraded to S3)
- Email: Console logging (can be upgraded to Resend)

---

## 🚀 Production Deployment

### Railway + Vercel Setup
- **Backend**: Deployed on Railway with Python 3.14
- **Frontend**: Deployed on Vercel
- **Database**: PostgreSQL on Railway
- **Production CORS**: Configured for cross-origin requests
- **Environment Variables**: Production-specific env vars configured

### Deployment Features
- Auto-deploy on git push
- Production-grade logging
- Health check endpoints
- Database auto-migration on startup

---

## ✅ COMPLETED WORK

### Phase 1: Foundation (COMPLETE) ✅

**Infrastructure**:
- ✅ Docker Compose with PostgreSQL and Redis
- ✅ All frontend dependencies installed
- ✅ All backend dependencies installed via uv
- ✅ SQLAlchemy models created for all 4 pillars
- ✅ Database tables initialized
- ✅ Database reset utility for schema updates
- ✅ Auto-table creation on startup (safe, won't delete data)

**Database Improvements**:
- ✅ Seed script creates multiple accounts per role (2 Faculty, 2 Authority, 2 Student)
- ✅ Sample data for all 4 pillars (courses, grievances, opportunities)
- ✅ Safe initialization - tables created automatically without data loss

**File Storage**:
- ✅ Local file storage configured in `/backend/uploads/`
- ✅ Separate directories for: grievances, courses, opportunities, avatars
- ✅ File upload endpoints implemented and working
- ✅ S3 migration guide created (`MIGRATE_TO_S3.md`)

**Frontend Components**:
- ✅ shadcn/ui setup
- ✅ Toast notifications (sonner)
- ✅ All required UI components (Button, Card, Input, Label, Badge, Tabs, Select)
- ✅ Lucide icons installed

**Backend**:
- ✅ FastAPI app structure
- ✅ JWT authentication system
- ✅ Password hashing with bcrypt
- ✅ Role-based access control (STUDENT, FACULTY, AUTHORITY, ADMIN)
- ✅ CORS configured
- ✅ Environment variables configured

### Phase 2: Identity & Governance (COMPLETE) ✅

**Pages Built**:
- ✅ Landing Page (/) - Marketing site with 4 pillars, CTA, features
- ✅ Login Page (/login) - Form with validation
- ✅ Register Page (/register) - Role selection, email validation, department dropdown
- ✅ Profile Page (/profile) - View/edit profile, change password, department dropdown

**Features**:
- ✅ Email domain validation:
  - STUDENT: @students.iitmandi.ac.in only
  - FACULTY/AUTHORITY/ADMIN: @iitmandi.ac.in only
- ✅ ADMIN self-registration prevented (only existing admins can promote)
- ✅ JWT token generation (access + refresh)
- ✅ Auth store with Zustand
- ✅ API client with axios and interceptors
- ✅ Responsive design
- ✅ Toast notifications for feedback
- ✅ Department dropdown in registration and profile

**API Endpoints Working**:
- POST /api/v1/auth/register - User registration with role validation
- POST /api/v1/auth/login - User login
- POST /api/v1/auth/refresh - Token refresh
- POST /api/v1/auth/logout - Logout
- GET /api/v1/users/me - Get current user profile
- PUT /api/v1/users/me - Update profile
- POST /api/v1/users/me/change-password - Change password
- GET /api/v1/users/ - List all users (admin only)
- PUT /api/v1/users/{id}/role - Update user role with email validation (admin only)

### Phase 3: Voice - Grievance System (COMPLETE) ✅

**Pages Built**:
- ✅ Grievances List (/grievances) - Connected to API with search/filter
- ✅ New Grievance Form (/grievances/new) - Full form with validation, connected to API
  - Category dropdown (Infrastructure, Academics, Hostel, Food, Other)
  - Priority selector (Low, Medium, High, Urgent)
  - Location input
  - Title & description
  - Photo upload UI
  - Anonymous toggle
- ✅ Grievance Detail (/grievances/[id]) - With timeline

**Features**:
- ✅ Create grievance with anonymous option
- ✅ List grievances with filters (status, category)
- ✅ View grievance details with full timeline
- ✅ AUTHORITY can view and update ALL grievances
- ✅ Faculty/Authority/Admin can add status updates
- ✅ Automatic assignment on first update

**API Endpoints Working**:
- POST /api/v1/grievances/ - Create grievance
- GET /api/v1/grievances/ - List grievances (students see own+anonymous, staff see all)
- GET /api/v1/grievances/{id} - Get grievance details
- POST /api/v1/grievances/{id}/updates - Add status update (faculty/authority/admin only)
- POST /api/v1/grievances/{id}/photos - Upload photo

### Phase 4: Fate - Academic System (COMPLETE) ✅

**Pages Built**:
- ✅ Courses List (/courses) - Connected to API with search/filter
- ✅ Course Detail (/courses/[id]) - With enrollment check
  - Shows course info only if enrolled, professor, or admin
  - Shows "Enroll Now" button if not enrolled
  - Tabs for resources, assignments, grades

**Features**:
- ✅ Create courses (faculty auto-assigned as professor, admin can create without professor)
- ✅ List all courses with filters (department, semester)
- ✅ Enrollment system (students only)
- ✅ Course detail access control (enrolled students, professor, or admin)
- ✅ Resource upload restricted to course professor only
- ✅ View course resources

**API Endpoints Working**:
- POST /api/v1/courses/ - Create course (faculty/admin only)
- GET /api/v1/courses/ - List all courses
- GET /api/v1/courses/{id} - Get course details (enforcement check)
- POST /api/v1/courses/{id}/enroll - Enroll in course (students only)
- GET /api/v1/courses/{id}/resources - List resources
- POST /api/v1/courses/{id}/resources - Upload resource (professor only)
- GET /api/v1/courses/{id}/calendar - List calendar events
- GET /api/v1/courses/my/enrollments - Get my enrollments

### Phase 5: Opportunity System (COMPLETE) ✅

**Pages Built**:
- ✅ Opportunities List (/opportunities) - Connected to API with filtering

**Features**:
- ✅ Create opportunities with type (RESEARCH/INTERNSHIP)
- ✅ Both FACULTY and AUTHORITY can create opportunities
- ✅ List all open opportunities
- ✅ Apply to opportunities (students only)
- ✅ Application status tracking
- ✅ Faculty/Authority can view applications for their opportunities
- ✅ Update application status
- ✅ Task Manager (Scholar's Ledger) - Full CRUD for personal tasks

**API Endpoints Working**:
- POST /api/v1/opportunities/ - Create opportunity (faculty/authority only)
- GET /api/v1/opportunities/ - List opportunities
- GET /api/v1/opportunities/{id} - Get opportunity details
- PUT /api/v1/opportunities/{id}/close - Close opportunity (owner or admin)
- POST /api/v1/opportunities/{id}/apply - Apply to opportunity (students only)
- GET /api/v1/opportunities/{id}/applications - List applications (owner or admin)
- PUT /api/v1/opportunities/applications/{id}/status - Update application status
- GET /api/v1/opportunities/my/applications - Get my applications
- GET /api/v1/opportunities/my/tasks - List my tasks
- POST /api/v1/opportunities/my/tasks - Create task
- PUT /api/v1/opportunities/my/tasks/{id} - Update task
- DELETE /api/v1/opportunities/my/tasks/{id} - Delete task

### Phase 6: Latest Features (COMPLETE) ✅

**UI Improvements**:
- ✅ Department dropdown in registration and profile pages
- ✅ Enhanced error handling for different backend error formats (string, array, object)
- ✅ Debug logging for troubleshooting API issues
- ✅ Production-ready CORS configuration

**Developer Experience**:
- ✅ Comprehensive seed data for testing
- ✅ Multiple test accounts per role
- ✅ S3 migration documentation

---

## 📊 ROLE-BASED PERMISSIONS

### STUDENT (@students.iitmandi.ac.in)
- Submit grievances (anonymous option)
- View own grievances + anonymous grievances
- Browse all courses
- Enroll in courses
- View enrolled course details
- Apply to opportunities
- Manage personal tasks (Scholar's Ledger)
- View application status

### FACULTY (@iitmandi.ac.in)
- Everything students can do
- Create courses (auto-assigned as professor)
- Upload resources to own courses only
- Create opportunities (RESEARCH or INTERNSHIP)
- View applications for own opportunities
- Update application status
- Update grievance status

### AUTHORITY (@iitmandi.ac.in)
- Everything students can do
- **Manage ALL grievances** across entire institute
- Create opportunities (RESEARCH or INTERNSHIP)
- View applications for own opportunities
- Update application status
- View all courses

### ADMIN (@iitmandi.ac.in)
- **Full system access**
- Create courses without being professor
- Close any opportunity
- View any application
- Manage all users (list all, change roles)
- Override all ownership restrictions

**Security**: ADMIN role cannot be self-assigned. Only existing admins can promote users to ADMIN via the user management API.

---

## 📁 Project Structure

```
krkhc_2/
├── docker-compose.yml          # PostgreSQL + Redis
├── .env                        # DB credentials
├── PROJECT_STATUS.md          # This file
├── backend/                    # FastAPI Backend
│   ├── main.py                # FastAPI app entry
│   ├── init_db.py             # Database initialization
│   ├── reset_db.py            # Database reset utility
│   ├── start.sh               # Startup script
│   ├── pyproject.toml         # uv dependencies
│   ├── .env                   # Backend env vars
│   └── app/
│       ├── core/              # Config, security, deps
│       │   ├── config.py      # Settings
│       │   ├── security.py    # JWT, bcrypt
│       │   └── deps.py        # Auth dependencies
│       ├── models/            # SQLAlchemy models
│       │   ├── user.py        # User model with roles
│       │   ├── grievance.py   # Grievance + GrievanceUpdate
│       │   ├── academic.py    # Course, Enrollment, Resource, Calendar
│       │   └── opportunity.py # Opportunity, Application, Task
│       └── api/               # API routes
│           ├── auth.py        # Auth endpoints + ADMIN prevention
│           ├── users.py       # User management + role changes
│           ├── grievances.py  # Grievance CRUD + updates
│           ├── courses.py     # Course CRUD + enrollment + resources
│           └── opportunities.py # Opportunity + Application + Tasks
├── frontend/                   # Next.js Frontend
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.ts
│   ├── app/
│   │   ├── layout.tsx         # Root layout with toast
│   │   ├── page.tsx           # Landing page
│   │   ├── globals.css        # Tailwind + CSS vars
│   │   ├── (auth)/            # Auth route group
│   │   │   ├── login/page.tsx
│   │   │   └── register/page.tsx  # With department dropdown
│   │   └── (dashboard)/       # Dashboard route group
│   │       ├── layout.tsx     # Dashboard layout
│   │       ├── dashboard/page.tsx
│   │       ├── profile/page.tsx   # With department dropdown
│   │       ├── grievances/
│   │       │   ├── page.tsx       # Connected to API
│   │       │   ├── new/page.tsx   # Connected to API
│   │       │   └── [id]/page.tsx
│   │       ├── courses/
│   │       │   ├── page.tsx       # Connected to API
│   │       │   └── [id]/page.tsx  # With enrollment check
│   │       └── opportunities/
│   │           └── page.tsx       # Connected to API
│   ├── components/
│   │   ├── ui/                # shadcn components
│   │   └── layout/
│   │       └── dashboard-layout.tsx
│   ├── lib/
│   │   ├── utils.ts           # cn helper
│   │   └── api.ts             # Axios client + all API functions
│   └── stores/
│       └── auth.ts            # Zustand auth store
└── AEGIS_TechStack.docx       # Technical requirements
    Web-Dev.pdf                # Competition requirements
```

---

## 🔧 Backend Configuration

**Environment Variables** (`backend/.env`):
```env
DATABASE_URL=postgresql+asyncpg://aegis_user:aegis_password@localhost:5432/aegis_db
REDIS_URL=redis://localhost:6379
JWT_SECRET=your-super-secret-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7
```

**Running Backend**:
```bash
cd /home/apsingh/Documents/krkhc_2/backend
./start.sh
# OR
source .venv/bin/activate && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**API Documentation**:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

**Tested & Working**:
- User registration with email domain validation
- User login with JWT tokens
- Password hashing with bcrypt
- All 4 pillar APIs fully functional
- Role-based access control

---

## 🚀 Running the Project

**Prerequisites**:
- Docker & Docker Compose
- Node.js + npm
- uv (Python package manager)
- Python 3.14+

**Step 1: Start Infrastructure**:
```bash
cd /home/apsingh/Documents/krkhc_2
docker-compose up -d
```

**Step 2: Initialize Database** (first time or after schema changes):
```bash
cd /home/apsingh/Documents/krkhc_2/backend
source .venv/bin/activate
python init_db.py
# OR reset everything:
python reset_db.py
```

**Step 3: Start Backend**:
```bash
cd /home/apsingh/Documents/krkhc_2/backend
./start.sh
```

**Step 4: Start Frontend**:
```bash
cd /home/apsingh/Documents/krkhc_2/frontend
npm run dev
```

**Access**:
- Landing: http://localhost:3000
- Login: http://localhost:3000/login
- API Docs: http://localhost:8000/docs

---

## 🎯 Core Pillars Status

**Pillar I: Identity & Governance** ✅ COMPLETE
- Role-based auth (Student, Faculty, Authority, Admin)
- Email domain validation (@students.iitmandi.ac.in vs @iitmandi.ac.in)
- ADMIN self-registration prevention
- User management API (admin only)
- Profile management with department dropdown

**Pillar II: Voice** ✅ COMPLETE
- Grievance submission (anonymous option)
- Status tracking with timeline
- AUTHORITY can manage ALL grievances
- Photo upload capability
- Status workflow: SUBMITTED → UNDER_REVIEW → IN_PROGRESS → RESOLVED

**Pillar III: Fate** ✅ COMPLETE
- Course enrollment system
- Resource repository (professor-only upload)
- Academic calendar
- Enrollment-based access control
- Professor ownership of courses

**Pillar IV: Opportunity** ✅ COMPLETE
- Faculty & Authority can post opportunities (RESEARCH/INTERNSHIP types)
- Student applications with status tracking
- Application management by opportunity owners
- Task Manager (Scholar's Ledger) with full CRUD

---

## 🎨 Design Decisions

**Theme**: Clean, modern, professional
**Colors**: Blue primary, neutral grays
**Typography**: Geist font (from Next.js)
**Responsive**: Mobile-first, works on all devices
**Components**: shadcn/ui with custom styling

---

## 🔐 Security Features

- JWT tokens (15 min access, 7 day refresh)
- Passwords hashed with bcrypt
- Email domain validation:
  - Students: @students.iitmandi.ac.in only
  - Staff: @iitmandi.ac.in only
- Role-based access control with granular permissions
- ADMIN self-registration prevented
- Email validation on role changes
- Course professor-only resource upload
- Enrollment-based course detail access
- CORS configured for localhost:3000

---

## 🐛 Known Issues

1. ✅ **All critical issues resolved**
2. ✅ File upload working with local storage (S3 migration guide available)
3. Next.js params now use React.use() for unwrapping (Next.js 16 requirement)

---

## 📚 Key Information from Documents

**From PDF (Requirements)**:
- 4 Core Pillars (mandatory): Identity, Voice, Fate, Opportunity
- 3 Bonus Pillars (optional): Commons, Connection, Spirit
- Evaluation: 40% pillar completeness, 25% UX, 20% architecture, 15% innovation
- Must use IIT Mandi emails
- Team size: 2-4 members

**From DOCX (Tech Stack)**:
- Frontend: Next.js 16, TypeScript, Tailwind, shadcn/ui, TanStack Query, Zustand
- Backend: FastAPI, SQLAlchemy 2.0, PostgreSQL, Redis
- Auth: JWT
- File Storage: Local (S3 ready)

---

## 🚀 Remaining Work (Optional Enhancements)

### Phase 6: Community Features (Bonus Pillars V-VII)

**Pillar V - The Commons**:
- Ride Sharing (Caravan Pool)
- Lost & Found (Relic Recovery)

**Pillar VI - Connection**:
- Forum (Hall of Echoes)
- Campus Map (Pathfinder)
- SOS Emergency (Guardian's Flare)

**Pillar VII - The Spirit**:
- Clubs (Guild Halls)
- Announcements (Universal Array)

### Phase 7: Dashboards & Polish

**Dashboards**:
- Student Dashboard with real data
- Faculty Dashboard
- Admin Dashboard with user management

**Polish**:
- File storage implementation (S3)
- Email notifications
- Real-time updates (WebSockets)
- Advanced search and filtering
- Export functionality

---

## 📝 Quick Commands Reference

```bash
# Start everything
cd /home/apsingh/Documents/krkhc_2
docker-compose up -d
cd backend && ./start.sh
cd frontend && npm run dev

# Database
docker exec aegis-postgres psql -U aegis_user -d aegis_db -c "\dt"

# Backend test
curl http://localhost:8000/health

# Database reset (after schema changes)
cd backend && source .venv/bin/activate && python reset_db.py

# Install frontend deps
cd frontend && npm install <package>

# Install backend deps
cd backend && uv add <package>
```

---

## 👥 Test Accounts

All accounts use password: `password123`

**Faculty (2 accounts)**:
- faculty1@iitmandi.ac.in
- faculty2@iitmandi.ac.in
- Can: Create courses, create opportunities, manage own content

**Authority (2 accounts)**:
- authority1@iitmandi.ac.in
- authority2@iitmandi.ac.in
- Can: Manage all grievances, create opportunities

**Student (2 accounts)**:
- student1@students.iitmandi.ac.in
- student2@students.iitmandi.ac.in
- Can: Submit grievances, enroll in courses, apply to opportunities

**Admin (1 account)**:
- admin@iitmandi.ac.in
- Can: Everything including user management

---

## 💬 Important Notes

1. ✅ **ALL 4 CORE PILLARS ARE FUNCTIONAL** - Backend APIs complete, frontend connected
2. ✅ **Role-based permissions fully implemented** - Each role has appropriate access
3. ✅ **Email domain validation working** - Students use @students.iitmandi.ac.in
4. ✅ **Security hardened** - ADMIN cannot self-register, professor-only uploads
5. ✅ **Frontend responsive** - Works on mobile and desktop
6. ✅ **Ready for demo** - All core features working end-to-end

**For File Upload**: Backend endpoints exist but storage needs configuration (local or S3)

---

**Document Version**: 2.1  
**Status**: Production Deployed ✅  
**Date**: February 15, 2026

---

## 🎉 Achievement Summary

✅ **Pillar I (Identity)**: Complete with role-based auth  
✅ **Pillar II (Voice)**: Complete with grievance system  
✅ **Pillar III (Fate)**: Complete with course system  
✅ **Pillar IV (Opportunity)**: Complete with opportunities + task manager  
✅ **Production**: Deployed on Railway + Vercel  

**Total**: 4/4 Core Pillars Complete (100%) + Production Live

Live URLs:
- Frontend: https://aegis-protocol-krkhc.vercel.app
- Backend: https://krkhc-production.up.railway.app

Ready for submission! 🚀
