import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth.models.user import Base, User
from auth.utils.password import PasswordUtil

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def client():
    from main import app
    return TestClient(app)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

def test_user_registration(client, db_session):
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "TestPass123!",
        "first_name": "Test",
        "last_name": "User"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_user_login(client, db_session):
    """Test user login"""
    # Create user
    user = User(
        email="test@example.com",
        hashed_password=PasswordUtil.hash_password("TestPass123!")
    )
    db_session.add(user)
    db_session.commit()

    # Login
    response = client.post("/api/auth/login", data={
        "username": "test@example.com",
        "password": "TestPass123!"
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_invalid_login(client, db_session):
    """Test invalid login credentials"""
    response = client.post("/api/auth/login", data={
        "username": "nonexistent@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401
