import pytest
import tempfile
import os

@pytest.fixture
def temp_json_file():
    """Create temporary JSON file for testing"""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    yield path
    os.unlink(path)

@pytest.fixture
def sample_appointment_data():
    """Provide valid appointment test data"""
    return {
        'patient_id': 1,
        'doctor_id': 2,
        'appointment_time': '2024-01-15T14:00:00',
        'duration_minutes': 30,
        'status': 'scheduled'
    }
