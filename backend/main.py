from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.config import get_settings
from app.core.storage import UPLOAD_DIR
from app.api import auth, users, grievances, courses, opportunities, files

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="AEGIS Platform - Unified Digital Citadel for IIT Mandi",
    version="0.1.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for local file serving
app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

# Include routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(grievances.router, prefix="/api/v1")
app.include_router(courses.router, prefix="/api/v1")
app.include_router(opportunities.router, prefix="/api/v1")
app.include_router(files.router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Welcome to AEGIS Platform API",
        "version": "0.1.0",
        "status": "operational",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
