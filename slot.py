from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class Slot(BaseModel):
    id: Optional[str] = Field(default=None, description="Unique slot identifier")
    start_time: datetime = Field(..., description="Slot start datetime")
    end_time: datetime = Field(..., description="Slot end datetime")
    therapist_id: str = Field(..., description="Therapist email/identifier")
    is_available: bool = Field(default=True, description="Slot availability status")
    appointment_id: Optional[str] = Field(default=None, description="Linked appointment ID")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SlotCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    therapist_id: str

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SlotUpdate(BaseModel):
    is_available: bool = Field(default=True)
