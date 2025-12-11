from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import CRUDBase
from .db import get_db
from .models import Staff
from .schemas import StaffCreate, StaffOut, StaffUpdate

router = APIRouter(prefix="/staff", tags=["Staff"])
crud = CRUDBase[Staff](Staff)


@router.get("/", response_model=List[StaffOut], summary="List staff")
# PUBLIC_INTERFACE
async def list_staff(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
):
    """List staff members."""
    return await crud.list(db, skip=skip, limit=limit)


@router.get("/{staff_id}", response_model=StaffOut, summary="Get staff member")
# PUBLIC_INTERFACE
async def get_staff(staff_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):
    """Get staff by ID."""
    staff = await crud.get(db, staff_id)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return staff


@router.post("/", response_model=StaffOut, status_code=status.HTTP_201_CREATED, summary="Create staff")
# PUBLIC_INTERFACE
async def create_staff(payload: StaffCreate, db: AsyncSession = Depends(get_db)):
    """Create staff."""
    return await crud.create(db, payload.model_dump())


@router.put("/{staff_id}", response_model=StaffOut, summary="Update staff")
# PUBLIC_INTERFACE
async def update_staff(
    staff_id: int = Path(..., ge=1), payload: StaffUpdate = None, db: AsyncSession = Depends(get_db)
):
    """Update staff."""
    staff = await crud.get(db, staff_id)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return await crud.update(db, staff, payload.model_dump())


@router.patch("/{staff_id}", response_model=StaffOut, summary="Patch staff")
# PUBLIC_INTERFACE
async def patch_staff(
    staff_id: int = Path(..., ge=1), payload: StaffUpdate = None, db: AsyncSession = Depends(get_db)
):
    """Patch staff."""
    staff = await crud.get(db, staff_id)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    return await crud.update(db, staff, payload.model_dump(exclude_unset=True))


@router.delete("/{staff_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete staff")
# PUBLIC_INTERFACE
async def delete_staff(staff_id: int = Path(..., ge=1), db: AsyncSession = Depends(get_db)):
    """Delete staff."""
    staff = await crud.get(db, staff_id)
    if not staff:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    await crud.delete(db, staff)
    return None
