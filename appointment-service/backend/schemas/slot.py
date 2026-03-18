from pydantic import BaseModel, Field, validator
from datetime import date, time
from typing import Optional

class SlotBase(BaseModel):
    location: str = Field(..., max_length=100)
    date: date
    time: time
    capacity: int = Field(..., ge=1)

    @validator('date')
    def validate_date(cls, v):
        from datetime import datetime
        if v < date.today():
            raise ValueError('Date must be in the future')
        return v

    @validator('time')
    def validate_time(cls, v):
        if not (0 <= v.hour < 24 and 0 <= v.minute < 60):
            raise ValueError('Invalid time format')
        return v

class SlotCreate(SlotBase):
    pass

class SlotUpdate(SlotBase):
    pass

class SlotResponse(SlotBase):
    id: int
    is_available: bool
    created_by: int

    class Config:
        from_attributes = True

class SlotList(BaseModel):
    slots: list[SlotResponse]
