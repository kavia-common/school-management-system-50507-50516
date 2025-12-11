from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CRUDBase
from .db import get_db
from .models import Student
from .schemas import StudentCreate, StudentOut, StudentUpdate

router = APIRouter(prefix="/students", tags=["Students"])
crud = CRUDBase[Student](Student)


@router.get("/", response_model=List[StudentOut], summary="List students")
# PUBLIC_INTERFACE
async def list_students(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """List students."""
    return await crud.list(db, skip=skip, limit=limit)


@router.get("/{student_id}", response_model=StudentOut, summary="Get student")
# PUBLIC_INTERFACE
async def get_student(student_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):
    """Get student by ID."""
    student = await crud.get(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return student


@router.post("/", response_model=StudentOut, status_code=status.HTTP_201_CREATED, summary="Create student")
# PUBLIC_INTERFACE
async def create_student(payload: StudentCreate, db: AsyncSession = Depends(get_db)):
    """Create student."""
    return await crud.create(db, payload.model_dump())


@router.put("/{student_id}", response_model=StudentOut, summary="Update student")
# PUBLIC_INTERFACE
async def update_student(
    student_id: int = Path(..., ge=1), payload: StudentUpdate = None, db: AsyncSession = Depends(get_db)
):
    """Update student."""
    student = await crud.get(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return await crud.update(db, student, payload.model_dump())


@router.patch("/{student_id}", response_model=StudentOut, summary="Patch student")
# PUBLIC_INTERFACE
async def patch_student(
    student_id: int = Path(..., ge=1), payload: StudentUpdate = None, db: AsyncSession = Depends(get_db)
):
    """Patch student."""
    student = await crud.get(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    return await crud.update(db, student, payload.model_dump(exclude_unset=True))


@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete student")
# PUBLIC_INTERFACE
async def delete_student(student_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):
    """Delete student."""
    student = await crud.get(db, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")
    await crud.delete(db, student)
    return None
