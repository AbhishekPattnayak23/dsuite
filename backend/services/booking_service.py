from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
from backend.models.slot import Slot, UserAppointment
from backend.services.email_service import EmailService
import logging
import threading

logger = logging.getLogger(__name__)

# Local locks for preventing double-booking
booking_locks = threading.Lock()

class BookingService:
    def __init__(self, db: Session):
        self.db = db
        self.email_service = EmailService()

    def search_slots(self, location: str, date: str) -> list:
        """Search available slots by location and date"""
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
            start_time = target_date.replace(hour=0, minute=0, second=0)
            end_time = target_date.replace(hour=23, minute=59, second=59)

            slots = self.db.query(Slot).filter(
                and_(
                    Slot.location.ilike(f"%{location}%"),
                    Slot.start_time >= start_time,
                    Slot.start_time <= end_time,
                    Slot.is_available == True,
                    Slot.booked_count < Slot.capacity
                )
            ).order_by(Slot.start_time).all()

            return [{
                "id": slot.id,
                "location": slot.location,
                "start_time": slot.start_time.isoformat(),
                "end_time": slot.end_time.isoformat(),
                "available_capacity": slot.capacity - slot.booked_count
            } for slot in slots]

        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise

    def book_slot(self, slot_id: int, user_email: str, user_name: str) -> dict:
        """Book a slot with local locking to prevent double-booking"""
        global booking_locks

        with booking_locks:
            try:
                # Get slot with row-level lock
                slot = self.db.query(Slot).filter(
                    Slot.id == slot_id
                ).with_for_update(nowait=True).first()

                if not slot:
                    raise ValueError("Slot not found")

                if slot.booked_count >= slot.capacity:
                    raise ValueError("Slot is fully booked")

                # Create appointment
                appointment = UserAppointment(
                    slot_id=slot_id,
                    user_email=user_email,
                    user_name=user_name
                )

                # Update slot
                slot.booked_count += 1
                if slot.booked_count >= slot.capacity:
                    slot.is_available = False

                self.db.add(appointment)
                self.db.commit()

                # Send confirmation email
                email_details = {
                    'user_name': user_name,
                    'location': slot.location,
                    'date': slot.start_time.strftime("%B %d, %Y"),
                    'time': slot.start_time.strftime("%I:%M %p"),
                    'booking_id': appointment.id
                }

                self.email_service.send_confirmation_email(user_email, email_details)

                return {
                    'success': True,
                    'booking_id': appointment.id,
                    'slot_id': slot_id,
                    'confirmation_sent': True
                }

            except ValueError as e:
                self.db.rollback()
                raise
            except Exception as e:
                self.db.rollback()
                logger.error(f"Booking failed: {e}")
                raise
