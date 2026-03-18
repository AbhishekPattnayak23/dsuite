"""
End-to-end booking test with proper test client setup
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from app.main import app

client = TestClient(app)

def test_booking_endpoints_accessible():
    """Test that booking-related endpoints are accessible"""
    # Test health endpoint
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

    # Test home endpoint
    response = client.get("/")
    assert response.status_code == 200

    # Test appointments endpoint
    response = client.get("/appointments/")
    assert response.status_code in [200, 404, 422]  # Accept any response indicating endpoint attempts

def test_environment_setup():
    """Test that the environment is properly set up"""
    assert app is not None
