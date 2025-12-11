from contextlib import asynccontextmanager
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import engine
from .models import Base
from .routers_teachers import router as teachers_router
from .routers_students import router as students_router
from .routers_exams import router as exams_router
from .routers_staff import router as staff_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup if they do not exist
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Optional: dispose engine on shutdown
    await engine.dispose()


app = FastAPI(
    title="School Management System API",
    description="FastAPI backend for managing Teachers, Students, Exams, and Staff.",
    version="1.0.0",
    lifespan=lifespan,
    openapi_tags=[
        {"name": "Teachers", "description": "Teacher management endpoints"},
        {"name": "Students", "description": "Student management endpoints"},
        {"name": "Exams", "description": "Examination management endpoints"},
        {"name": "Staff", "description": "Staff management endpoints"},
    ],
)

allowed_origins = os.environ.get(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,https://vscode-internal-15220-qa.qa01.cloud.kavia.ai:3000",
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in allowed_origins if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", summary="Health Check", tags=["Health"])
def health_check():
    """Simple service health check endpoint."""
    return {"message": "Healthy"}


# Register routers
app.include_router(teachers_router)
app.include_router(students_router)
app.include_router(exams_router)
app.include_router(staff_router)
