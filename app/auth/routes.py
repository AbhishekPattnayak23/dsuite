"""
Authentication routes for the application
"""
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import logging

router = APIRouter(prefix="/auth", tags=["authentication"])

logger = logging.getLogger(__name__)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    """Basic login endpoint for testing"""
    try:
        if user.email == "test@example.com" and user.password == "password123":
            return {"access_token": "fake-jwt-token-for-testing", "token_type": "bearer"}
        else:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/me")
async def get_current_user():
    """Get current user endpoint"""
    return {"email": "test@example.com", "id": 1, "name": "Test User"}
