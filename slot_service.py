import logging
from datetime import datetime, timedelta
from typing import List, Optional
from slot import Slot, SlotCreate, SlotUpdate
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SlotService:
    def __init__(self):
        self.slots = {}
        logger.info("SlotService initialized successfully")

    async def create_slot(self, slot_data: SlotCreate) -> Slot:
        try:
            slot_id = str(uuid.uuid4())

            # Validate times
            if slot_data.start_time >= slot_data.end_time:
                raise ValueError("End time must be after start time")

            # Create 30-minute slots by default
            slots = []
            current_time = slot_data.start_time

            while current_time < slot_data.end_time:
                end_time = current_time + timedelta(minutes=30)

                slot = Slot(
                    id=str(uuid.uuid4()),
                    start_time=current_time,
                    end_time=end_time,
                    therapist_id=slot_data.therapist_id
                )

                self.slots[slot.id] = slot
                slots.append(slot)
                logger.info(f"Created slot {slot.id} for {slot.therapist_id}")

                current_time = end_time

            return slots[0]  # Return first slot as example

        except Exception as e:
            logger.error(f"Failed to create slot: {e}")
            raise

    async def get_available_slots(self, therapist_id: str, date: datetime) -> List[Slot]:
        try:
            date_start = date.replace(hour=0, minute=0, second=0, microsecond=0)
            date_end = date.replace(hour=23, minute=59, second=59, microsecond=999999)

            available_slots = [
                slot for slot in self.slots.values()
                if slot.therapist_id == therapist_id
                and slot.is_available
                and date_start <= slot.start_time <= date_end
            ]

            logger.info(f"Found {len(available_slots)} available slots for {therapist_id}")
            return available_slots

        except Exception as e:
            logger.error(f"Failed to get available slots: {e}")
            raise

    async def book_slot(self, slot_id: str, appointment_id: str) -> Slot:
        try:
            if slot_id not in self.slots:
                raise ValueError(f"Slot {slot_id} not found")

            slot = self.slots[slot_id]

            if not slot.is_available:
                raise ValueError(f"Slot {slot_id} is already booked")

            slot.is_available = False
            slot.appointment_id = appointment_id

            logger.info(f"Booked slot {slot_id} for appointment {appointment_id}")
            return slot

        except Exception as e:
            logger.error(f"Failed to book slot: {e}")
            raise

    async def cancel_slot_booking(self, slot_id: str) -> Slot:
        try:
            if slot_id not in self.slots:
                raise ValueError(f"Slot {slot_id} not found")

            slot = self.slots[slot_id]
            slot.is_available = True
            slot.appointment_id = None

            logger.info(f"Cancelled booking for slot {slot_id}")
            return slot

        except Exception as e:
            logger.error(f"Failed to cancel slot booking: {e}")
            raise

    async def get_slot_by_id(self, slot_id: str) -> Optional[Slot]:
        return self.slots.get(slot_id)
