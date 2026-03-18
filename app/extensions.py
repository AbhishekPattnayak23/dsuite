"""
Shared extensions and utilities for the application
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

try:
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logging.info("Database extensions initialized successfully")
except Exception as e:
    logging.error(f"Failed to initialize database extensions: {e}")
    # Fallback for testing
    engine = None
    SessionLocal = None
    Base = None
    logging.warning("Using fallback test configuration")
