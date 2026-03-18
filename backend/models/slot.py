from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.config.database import Base

class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    capacity = Column(Integer, default=1)
    booked_count = Column(Integer, default=0)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    appointments = relationship("UserAppointment", back_populates="slot")

class UserAppointment(Base):
    __tablename__ = "user_appointments"

    id = Column(Integer, primary_key=True, index=True)
    slot_id = Column(Integer, ForeignKey("slots.id"))
    user_email = Column(String, index=True)
    user_name = Column(String)
    booking_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="confirmed")  # confirmed, cancelled

    slot = relationship("Slot", back_populates="appointments")
