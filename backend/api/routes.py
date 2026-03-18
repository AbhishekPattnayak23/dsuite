from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import List
from backend.config.database import get_db
from backend.services.booking_service import BookingService

app = FastAPI()

# Pydantic models
class SlotSearchRequest(BaseModel):
    location: str
    date: str  # Format: "YYYY-MM-DD"

class SlotResponse(BaseModel):
    id: int
    location: str
    start_time: str
    end_time: str
    available_capacity: int

class BookingRequest(BaseModel):
    slot_id: int
    user_email: EmailStr
    user_name: str

class BookingResponse(BaseModel):
    success: bool
    booking_id: int
    slot_id: int
    confirmation_sent: bool

@app.post("/api/slots/search", response_model=List[SlotResponse])
def search_slots(request: SlotSearchRequest, db: Session = Depends(get_db)):
    """Search available slots by location and date"""
    try:
        service = BookingService(db)
        slots = service.search_slots(request.location, request.date)
        return slots
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/appointments/book", response_model=BookingResponse)
def book_appointment(request: BookingRequest, db: Session = Depends(get_db)):
    """Book an appointment and send confirmation email"""
    try:
        service = BookingService(db)
        result = service.book_slot(
            slot_id=request.slot_id,
            user_email=request.user_email,
            user_name=request.user_name
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}
