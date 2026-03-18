from pydantic import BaseModel, Field
from datetime import datetime

class SlotBase(BaseModel):
    start_time: datetime
    end_time: datetime
    is_available: bool = True
    slot_type: str = "standard"

class SlotCreate(SlotBase):
    pass

class SlotUpdate(BaseModel):
    start_time: datetime = None
    end_time: datetime = None
    is_available: bool = None
    slot_type: str = None

class SlotResponse(SlotBase):
    id: int

    class Config:
        from_attributes = True
