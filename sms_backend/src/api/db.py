import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

# PUBLIC_INTERFACE
def get_database_url() -> str:
    """Returns the database URL from environment variables.
    Requires POSTGRES_URL to be set in the environment (.env).
    """
    # We expect POSTGRES_URL like postgresql://host:port/dbname — convert to asyncpg driver
    raw = os.environ.get("POSTGRES_URL")
    if not raw:
        raise RuntimeError("POSTGRES_URL environment variable is required")
    if raw.startswith("postgresql://"):
        return raw.replace("postgresql://", "postgresql+asyncpg://", 1)
    if raw.startswith("postgres://"):
        return raw.replace("postgres://", "postgresql+asyncpg://", 1)
    return raw


DATABASE_URL = get_database_url()

engine: AsyncEngine = create_async_engine(DATABASE_URL, future=True, echo=False)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


# PUBLIC_INTERFACE
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async SQLAlchemy session."""
    async with AsyncSessionLocal() as session:
        yield session
