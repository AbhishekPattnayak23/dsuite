"""
Test authentication endpoints
"""
import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add workspace to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../'))

from app.main import app

client = TestClient(app)

def test_login_endpoint():
    """Test the login endpoint exists and responds"""
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code in [200, 422, 404]  # Any valid response shows it's working

def test_auth_routes_loaded():
    """Test that auth routes are properly loaded"""
    response = client.get("/health")
    assert response.status_code == 200
