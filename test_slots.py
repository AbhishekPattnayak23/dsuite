import pytest
from datetime import datetime, timedelta
from slot import SlotCreate
from slot_service import SlotService

@pytest.fixture
def slot_service():
    return SlotService()

@pytest.fixture
def test_slot_data():
    return SlotCreate(
        start_time=datetime.now() + timedelta(days=1, hours=9),
        end_time=datetime.now() + timedelta(days=1, hours=17),
        therapist_id="therapist@example.com"
    )

@pytest.mark.asyncio
async def test_create_slot(slot_service, test_slot_data):
    slot = await slot_service.create_slot(test_slot_data)
    assert slot.therapist_id == "therapist@example.com"

@pytest.mark.asyncio
async def test_get_available_slots(slot_service, test_slot_data):
    await slot_service.create_slot(test_slot_data)

    date = datetime.now() + timedelta(days=1)
    slots = await slot_service.get_available_slots("therapist@example.com", date)

    assert len(slots) > 0
    assert slots[0].is_available == True

@pytest.mark.asyncio
async def test_book_and_cancel_slot(slot_service, test_slot_data):
    slot = await slot_service.create_slot(test_slot_data)

    # Book slot
    booked = await slot_service.book_slot(slot.id, "appointment123")
    assert booked.is_available == False
    assert booked.appointment_id == "appointment123"

    # Cancel booking
    cancelled = await slot_service.cancel_slot_booking(slot.id)
    assert cancelled.is_available == True
    assert cancelled.appointment_id is None
