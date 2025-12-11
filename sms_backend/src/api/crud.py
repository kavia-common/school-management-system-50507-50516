from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .models import Base

ModelType = TypeVar("ModelType", bound=Base)


class CRUDBase(Generic[ModelType]):
    """Generic async CRUD base for SQLAlchemy models."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    # PUBLIC_INTERFACE
    async def get(self, db: AsyncSession, model_id: Any) -> Optional[ModelType]:
        """Get an entity by primary key."""
        result = await db.execute(select(self.model).where(self.model.id == model_id))
        return result.scalar_one_or_none()

    # PUBLIC_INTERFACE
    async def list(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> Sequence[ModelType]:
        """List entities with pagination."""
        result = await db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    # PUBLIC_INTERFACE
    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new entity."""
        instance = self.model(**obj_in)
        db.add(instance)
        await db.commit()
        await db.refresh(instance)
        return instance

    # PUBLIC_INTERFACE
    async def update(self, db: AsyncSession, db_obj: ModelType, obj_in: Dict[str, Any]) -> ModelType:
        """Update an entity."""
        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    # PUBLIC_INTERFACE
    async def delete(self, db: AsyncSession, db_obj: ModelType) -> None:
        """Delete an entity."""
        await db.delete(db_obj)
        await db.commit()
