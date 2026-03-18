from sqlalchemy import func
from app.extensions import db, redis_client
from app.appointments.models import Appointment
from app.notification.services import NotificationService

class AppointmentService:
    def book_appointment(self, user_id, slot_id):
        lock_key = f'booking_slot_{slot_id}'
        lock = redis_client.lock(lock_key, timeout=10)

        try:
            if lock.acquire(blocking_timeout=5):
                # Check if already booked by this user
                existing = Appointment.query.filter_by(user_id=user_id, slot_id=slot_id).first()
                if existing:
                    return None

                # Check availability
                from app.appointments.models import Slot
                slot = Slot.query.get(slot_id)
                if not slot:
                    return None

                booked_count = db.session.query(func.count(Appointment.id)).filter_by(slot_id=slot_id).scalar()
                if booked_count >= slot.capacity:
                    return None

                # Create appointment
                appointment = Appointment(user_id=user_id, slot_id=slot_id)
                db.session.add(appointment)
                db.session.commit()

                # Send email notification
                notification_service = NotificationService()
                notification_service.send_booking_confirmation(user_id, appointment)

                return appointment
            return None

        finally:
            if lock:
                lock.release()
