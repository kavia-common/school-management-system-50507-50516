# school-management-system-50507-50516

This workspace contains multiple containers for the School Management System.

Backend (sms_backend):
- FastAPI service with CRUD for Teachers, Students, Exams, and Staff.
- Uses SQLAlchemy async engine with PostgreSQL (asyncpg).

Environment configuration:
- Copy sms_backend/.env.example to sms_backend/.env and set values:
  - DATABASE_URL: PostgreSQL connection string.
    - Examples:
      - postgresql://user:pass@host:5432/dbname
      - postgres://user:pass@host:5432/dbname
    - The backend automatically converts to the async driver (postgresql+asyncpg://).
  - ALLOWED_ORIGINS: Comma-separated list of allowed CORS origins for the frontend.
    - Examples:
      - http://localhost:3000,http://127.0.0.1:5173
      - Use * during local development if needed.

CORS behavior:
- The backend reads ALLOWED_ORIGINS from environment.
- If not set, it defaults to "*" to simplify local development.
- Update ALLOWED_ORIGINS in production to a restricted list of your frontend origins.

HTTP status codes:
- Create endpoints return 201 Created.
- Delete endpoints return 204 No Content.

OpenAPI:
- Start the backend and visit /docs for interactive API docs.
- To regenerate a static OpenAPI file, run the generator script within sms_backend:
  - python -m src.api.generate_openapi