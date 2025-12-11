import os
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine

# PUBLIC_INTERFACE
def get_database_url() -> str:
    """Return the SQLAlchemy async database URL from environment variables.

    Expects DATABASE_URL to be set in the environment (.env). Examples:
      - DATABASE_URL=postgresql://user:pass@host:5432/dbname
      - DATABASE_URL=postgres://user:pass@host:5432/dbname

    The function will convert a synchronous Postgres URL to the asyncpg driver
    (postgresql+asyncpg://) as required by SQLAlchemy async engines.
    """
    raw = os.environ.get("DATABASE_URL")
    if not raw:
        raise RuntimeError("DATABASE_URL environment variable is required")
    # Normalize common postgres schemes to asyncpg
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
