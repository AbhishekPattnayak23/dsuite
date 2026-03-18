from __future__ import annotations
import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    appointments = db.relationship('Appointment', backref='user', lazy=True)

class Slot(db.Model):
    """Time slot for appointments."""
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    appointments = db.relationship('Appointment', backref='slot', lazy=True)

    __table_args__ = (UniqueConstraint('location', 'date'),)

class Appointment(db.Model):
    """Booking appointment."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    __table_args__ = (UniqueConstraint('user_id', 'slot_id'),)

class PasswordReset(db.Model):
    """Password reset tokens."""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    token = db.Column(db.String(64), unique=True, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)

def init_db():
    """Initialize database tables."""
    db.create_all()
