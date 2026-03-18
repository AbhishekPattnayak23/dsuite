import pytest
import json
from datetime import datetime
from app.appointments.models import Slot, Appointment
from app.models import User
from app.extensions import db, redis_client

@pytest.fixture
def client():
    from app import create_app
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def auth_token(client):
    # Create test user
    user = User(username='testuser', email='test@example.com', role='user')
    user.set_password('testpass')
    db.session.add(user)
    db.session.commit()

    # Login
    response = client.post('/api/auth/login', json={
        'email': 'test@example.com',
        'password': 'testpass'
    })
    return response.get_json()['token']

def test_slot_search_returns_snake_case(client, auth_token):
    # Create test slot
    slot = Slot(location='Test Center', date=datetime.strptime('2024-01-15', '%Y-%m-%d').date(), capacity=5)
    db.session.add(slot)
    db.session.commit()

    # Search slots
    response = client.get('/api/slots?location=Test',
                         headers={'Authorization': f'Bearer {auth_token}'})

    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) > 0

    # Check snake_case fields
    assert 'id' in data[0]
    assert 'location' in data[0]
    assert 'date' in data[0]
    assert 'capacity' in data[0]
    assert 'available' in data[0]

def test_atomic_booking_prevents_double_booking(client, auth_token):
    # Create test slot
    slot = Slot(location='Test Center', date=datetime.strptime('2024-01-15', '%Y-%m-%d').date(), capacity=1)
    db.session.add(slot)
    db.session.commit()

    # Concurrent booking attempts
    import threading
    results = []

    def book():
        response = client.post('/api/appointments',
                             headers={'Authorization': f'Bearer {auth_token}'},
                             json={'slot_id': slot.id})
        results.append(response.status_code)

    # Run 5 concurrent requests
    threads = []
    for _ in range(5):
        t = threading.Thread(target=book)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    # Only one should succeed
    success_count = results.count(201)
    failure_count = results.count(400)

    # Total should be 5 requests
    assert success_count == 1
    assert failure_count == 4

    # Verify only one appointment exists
    appointment_count = Appointment.query.filter_by(slot_id=slot.id).count()
    assert appointment_count == 1

def test_email_confirmation_and_redirect(client, auth_token):
    # Create test slot
    slot = Slot(location='Test Center', date=datetime.strptime('2024-01-15', '%Y-%m-%d').date(), capacity=2)
    db.session.add(slot)
    db.session.commit()

    # Book appointment
    response = client.post('/api/appointments',
                         headers={'Authorization': f'Bearer {auth_token}'},
                         json={'slot_id': slot.id})

    assert response.status_code == 201
    data = response.get_json()
    appointment_id = data['appointment']['id']

    # Verify appointment exists
    appointment = Appointment.query.get(appointment_id)
    assert appointment is not None

    # Check booking confirmation screen
    response = client.get(f'/booking-confirmation/{appointment_id}',
                         headers={'Authorization': f'Bearer {auth_token}'})

    assert response.status_code == 200
    assert 'Booking Confirmed' in response.data.decode()
