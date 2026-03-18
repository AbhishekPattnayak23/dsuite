from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    role = Column(String(10), default='user')
    created_at = Column(DateTime, default=datetime.utcnow)

class Slot(Base):
    __tablename__ = 'slots'

    id = Column(Integer, primary_key=True)
    location = Column(String(50), nullable=False)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    slot_id = Column(Integer, ForeignKey('slots.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    booked_at = Column(DateTime, default=datetime.utcnow)
    canceled = Column(Boolean, default=False)

    slot = relationship('Slot', backref='bookings')
    user = relationship('User', backref='bookings')

class Session(Base):
    __tablename__ = 'sessions'

    token = Column(String(64), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship('User', backref='sessions')
