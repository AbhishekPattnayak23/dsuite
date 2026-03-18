from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from app.core.database import get_db
from app.models.slot import Slot
from app.models.user import User
from app.schemas.slot import SlotCreate, SlotUpdate, SlotResponse
from app.middleware.auth import get_current_user, require_admin

router = APIRouter(prefix="/api/slots", tags=["slots"])

@router.get("/", response_model=List[SlotResponse])
async def get_available_slots(
    location: Optional[str] = Query(None, description="Filter by location"),
    booking_date: Optional[date] = Query(None, description="Filter by date"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get available slots (public access for authenticated users)"""
    query = db.query(Slot).filter(Slot.is_available == True)

    if location:
        query = query.filter(Slot.location.contains(location))
    if booking_date:
        query = query.filter(Slot.date == booking_date)

    slots = query.all()
    return slots

@router.post("/", response_model=SlotResponse)
async def create_slot(
    slot: SlotCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Create new slot (admin only)"""
    new_slot = Slot(
        location=slot.location,
        date=slot.date,
        time=slot.time,
        capacity=slot.capacity,
        is_available=True,
        created_by=current_user.id
    )

    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)

    return new_slot

@router.put("/{slot_id}", response_model=SlotResponse)
async def update_slot(
    slot_id: int,
    slot_update: SlotUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Update existing slot (admin only)"""
    slot = db.query(Slot).filter(Slot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    # Update fields
    slot.location = slot_update.location
    slot.date = slot_update.date
    slot.time = slot_update.time
    slot.capacity = slot_update.capacity

    db.commit()
    db.refresh(slot)

    return slot

@router.delete("/{slot_id}", response_model=dict)
async def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """Delete slot (admin only)"""
    slot = db.query(Slot).filter(Slot.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")

    db.delete(slot)
    db.commit()

    return {"message": "Slot deleted successfully"}
