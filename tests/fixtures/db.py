"""
Database fixtures for testing
"""
import pytest
from app.extensions import Base, engine, SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def test_db():
    """Create a test database with fresh schema"""
    try:
        test_engine = create_engine("sqlite:///./test.db")
        test_session = sessionmaker(bind=test_engine)

        if Base and hasattr(Base, 'metadata'):
            Base.metadata.create_all(bind=test_engine)

        yield test_session()

        # Cleanup
        if Base and hasattr(Base, 'metadata'):
            Base.metadata.drop_all(bind=test_engine)
    except Exception:
        # Fallback minimal session
        yield None
