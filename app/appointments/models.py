from datetime import datetime
from app.extensions import db

class Slot(db.Model):
    __tablename__ = 'slot'

    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    appointments = db.relationship('Appointment', backref='slot', lazy=True, cascade='all, delete-orphan')

    __table_args__ = (db.UniqueConstraint('location', 'date'),)

    @property
    def available(self):
        from sqlalchemy import func
        booked_count = db.session.query(func.count(Appointment.id)).filter_by(slot_id=self.id).scalar()
        return self.capacity - booked_count

class Appointment(db.Model):
    __tablename__ = 'appointment'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    slot_id = db.Column(db.Integer, db.ForeignKey('slot.id', ondelete='CASCADE'), nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'slot_id'),)
