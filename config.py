import os
from typing import Optional
from pydantic import BaseSettings, validator

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./appointments.db"

    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # App settings
    APP_NAME: str = "Appointment Booking API"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:3001"]

    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "your-secret-key-change-in-production" and not cls().DEBUG:
            raise ValueError("SECRET_KEY must be set in production")
        return v

    class Config:
        env_file = ".env"

settings = Settings()
