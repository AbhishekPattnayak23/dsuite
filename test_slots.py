import pytest
from fastapi.testclient import TestClient
from app import app
from database import engine, Base

Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_slot():
    response = client.post("/api/slots/", json={
        "start_time": "2024-01-01T09:00:00",
        "end_time": "2024-01-01T10:00:00",
        "is_available": True,
        "slot_type": "premium"
    })
    assert response.status_code == 201
    assert response.json()["slot_type"] == "premium"

def test_get_slots():
    response = client.get("/api/slots/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_slot():
    # First create a slot
    create_response = client.post("/api/slots/", json={
        "start_time": "2024-01-02T09:00:00",
        "end_time": "2024-01-02T10:00:00",
        "is_available": True
    })
    slot_id = create_response.json()["id"]

    response = client.get(f"/api/slots/{slot_id}")
    assert response.status_code == 200
    assert response.json()["id"] == slot_id

def test_update_slot():
    # Create slot
    create_response = client.post("/api/slots/", json={
        "start_time": "2024-01-03T09:00:00",
        "end_time": "2024-01-03T10:00:00"
    })
    slot_id = create_response.json()["id"]

    response = client.put(f"/api/slots/{slot_id}", json={
        "slot_type": "special"
    })
    assert response.status_code == 200
    assert response.json()["slot_type"] == "special"

def test_delete_slot():
    # Create slot
    create_response = client.post("/api/slots/", json={
        "start_time": "2024-01-04T09:00:00",
        "end_time": "2024-01-04T10:00:00"
    })
    slot_id = create_response.json()["id"]

    response = client.delete(f"/api/slots/{slot_id}")
    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f"/api/slots/{slot_id}")
    assert get_response.status_code == 404
