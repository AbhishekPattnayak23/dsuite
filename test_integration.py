"""Integration tests for agent/integration module"""
import pytest
import requests
import os
import sys

def test_python_path_configuration():
    """Test that Python path is correctly configured"""
    assert '/workspace' in sys.path

def test_dependencies_import():
    """Test all critical dependencies are available"""
    try:
        import requests
        import pytest
        import sqlalchemy
        import pydantic
        import fastapi
        dependency_check = True
    except ImportError as e:
        dependency_check = False
        print(f"Missing dependency: {e}")

    assert dependency_check is True

def test_database_schema_compatibility():
    """Test database schema compatibility"""
    from app.extensions import Base
    from sqlalchemy import Column, Integer, String

    class TestModel(Base):
        __tablename__ = 'test_model'
        id = Column(Integer, primary_key=True)
        name = Column(String(50))

    assert hasattr(TestModel, '__tablename__')
    assert TestModel.__tablename__ == 'test_model'

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
