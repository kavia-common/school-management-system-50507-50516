from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CRUDBase
from .db import get_db
from .models import Teacher
from .schemas import TeacherCreate, TeacherOut, TeacherUpdate

router = APIRouter(prefix="/teachers", tags=["Teachers"])
crud = CRUDBase[Teacher](Teacher)


@router.get(
    "/",
    response_model=List[TeacherOut],
    summary="List teachers",
    description="Retrieve a paginated list of teachers.",
)
# PUBLIC_INTERFACE
async def list_teachers(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
):
    """Return a list of teachers."""
    return await crud.list(db, skip=skip, limit=limit)


@router.get(
    "/{teacher_id}",
    response_model=TeacherOut,
    summary="Get teacher by ID",
    description="Retrieve a teacher by its unique identifier.",
)
# PUBLIC_INTERFACE
async def get_teacher(
    teacher_id: int = Path(..., ge=1, description="Teacher ID"),
    db: AsyncSession = Depends(get_db),
):
    """Return teacher details."""
    teacher = await crud.get(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return teacher


@router.post(
    "/",
    response_model=TeacherOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create teacher",
    description="Create a new teacher.",
)
# PUBLIC_INTERFACE
async def create_teacher(payload: TeacherCreate, db: AsyncSession = Depends(get_db)):
    """Create a teacher."""
    return await crud.create(db, payload.model_dump())


@router.put(
    "/{teacher_id}",
    response_model=TeacherOut,
    summary="Update teacher",
    description="Replace all fields of a teacher.",
)
# PUBLIC_INTERFACE
async def update_teacher(
    teacher_id: int = Path(..., ge=1),
    payload: TeacherUpdate = None,
    db: AsyncSession = Depends(get_db),
):
    """Update a teacher."""
    teacher = await crud.get(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return await crud.update(db, teacher, payload.model_dump())


@router.patch(
    "/{teacher_id}",
    response_model=TeacherOut,
    summary="Patch teacher",
    description="Update specific fields of a teacher.",
)
# PUBLIC_INTERFACE
async def patch_teacher(
    teacher_id: int = Path(..., ge=1),
    payload: TeacherUpdate = None,
    db: AsyncSession = Depends(get_db),
):
    """Patch a teacher."""
    teacher = await crud.get(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    return await crud.update(db, teacher, payload.model_dump(exclude_unset=True))


@router.delete(
    "/{teacher_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete teacher",
    description="Delete a teacher by ID.",
)
# PUBLIC_INTERFACE
async def delete_teacher(teacher_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):
    """Delete a teacher."""
    teacher = await crud.get(db, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Teacher not found")
    await crud.delete(db, teacher)
    return None
