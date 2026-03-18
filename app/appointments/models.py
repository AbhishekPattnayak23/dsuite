from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Slot(BaseModel):
    id: str
    start_time: datetime
    end_time: datetime
    is_available: bool = True

class Appointment(BaseModel):
    id: Optional[str] = None
    slot_id: str
    user_email: str
    user_name: str
    created_at: datetime = None

    def __init__(self, **data):
        super().__init__(**data)
        if self.created_at is None:
            self.created_at = datetime.utcnow()
