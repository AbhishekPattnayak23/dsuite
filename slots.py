from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, init_db
from schemas import SlotCreate, SlotUpdate, SlotResponse
from slot_service import SlotService

router = APIRouter(prefix="/api/slots", tags=["slots"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=SlotResponse, status_code=status.HTTP_201_CREATED)
def create_slot(slot: SlotCreate, db: Session = Depends(get_db)):
    try:
        return SlotService.create_slot(db, slot)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[SlotResponse])
def get_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return SlotService.get_slots(db, skip=skip, limit=limit)

@router.get("/{slot_id}", response_model=SlotResponse)
def get_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = SlotService.get_slot(db, slot_id)
    if not slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return slot

@router.put("/{slot_id}", response_model=SlotResponse)
def update_slot(slot_id: int, slot: SlotUpdate, db: Session = Depends(get_db)):
    updated_slot = SlotService.update_slot(db, slot_id, slot)
    if not updated_slot:
        raise HTTPException(status_code=404, detail="Slot not found")
    return updated_slot

@router.delete("/{slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_slot(slot_id: int, db: Session = Depends(get_db)):
    if not SlotService.delete_slot(db, slot_id):
        raise HTTPException(status_code=404, detail="Slot not found")
