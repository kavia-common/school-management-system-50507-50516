from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CRUDBase
from .db import get_db
from .models import Exam
from .schemas import ExamCreate, ExamOut, ExamUpdate

router = APIRouter(prefix="/exams", tags=["Exams"])
crud = CRUDBase[Exam](Exam)


@router.get("/", response_model=List[ExamOut], summary="List exams")
# PUBLIC_INTERFACE
async def list_exams(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """List exams."""
    return await crud.list(db, skip=skip, limit=limit)


@router.get("/{exam_id}", response_model=ExamOut, summary="Get exam")
# PUBLIC_INTERFACE
async def get_exam(exam_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):
    """Get exam by ID."""
    exam = await crud.get(db, exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return exam


@router.post("/", response_model=ExamOut, status_code=status.HTTP_201_CREATED, summary="Create exam")
# PUBLIC_INTERFACE
async def create_exam(payload: ExamCreate, db: AsyncSession = Depends(get_db)):
    """Create exam."""
    return await crud.create(db, payload.model_dump())


@router.put("/{exam_id}", response_model=ExamOut, summary="Update exam")
# PUBLIC_INTERFACE
async def update_exam(
    exam_id: int = Path(..., ge=1), payload: ExamUpdate = None, db: AsyncSession = Depends(get_db)
):
    """Update exam."""
    exam = await crud.get(db, exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return await crud.update(db, exam, payload.model_dump())


@router.patch("/{exam_id}", response_model=ExamOut, summary="Patch exam")
# PUBLIC_INTERFACE
async def patch_exam(
    exam_id: int = Path(..., ge=1), payload: ExamUpdate = None, db: AsyncSession = Depends(get_db)
):
    """Patch exam."""
    exam = await crud.get(db, exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    return await crud.update(db, exam, payload.model_dump(exclude_unset=True))


@router.delete("/{exam_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete exam")
# PUBLIC_INTERFACE
async def delete_exam(exam_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):
    """Delete exam."""
    exam = await crud.get(db, exam_id)
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")
    await crud.delete(db, exam)
    return None
