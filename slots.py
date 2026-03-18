from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import datetime
from slot import SlotCreate, SlotUpdate
from slot_service import SlotService

router = APIRouter()
slot_service = SlotService()

@router.post("/api/slots", response_model=dict)
async def create_slots(slot: SlotCreate):
    try:
        created_slot = await slot_service.create_slot(slot)
        return {"success": True, "slot": created_slot.dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/slots/available")
async def get_available_slots(
    therapist_id: str = Query(..., description="Therapist ID"),
    date: str = Query(..., description="Date in YYYY-MM-DD format")
):
    try:
        date_obj = datetime.strptime(date, "%Y-%m-%d")
        slots = await slot_service.get_available_slots(therapist_id, date_obj)
        return {"success": True, "slots": [slot.dict() for slot in slots]}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/slots/{slot_id}/book")
async def book_slot(slot_id: str, appointment_id: str = Query(...)):
    try:
        slot = await slot_service.book_slot(slot_id, appointment_id)
        return {"success": True, "slot": slot.dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/slots/{slot_id}/cancel")
async def cancel_slot(slot_id: str):
    try:
        slot = await slot_service.cancel_slot_booking(slot_id)
        return {"success": True, "slot": slot.dict()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/slots/{slot_id}")
async def get_slot(slot_id: str):
    try:
        slot = await slot_service.get_slot_by_id(slot_id)
        if not slot:
            raise HTTPException(status_code=404, detail="Slot not found")
        return {"success": True, "slot": slot.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
