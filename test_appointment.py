import requests
import json
from datetime import datetime, timedelta

API_BASE = "http://localhost:8000/api/v1"

def test_appointment_flow():
    """Test appointment creation and cancellation"""
    print("Testing appointment booking system...")

    # Sample appointment data
    appointment_data = {
        "user_id": 1,
        "staff_id": 1,
        "service_type": "Dental Checkup",
        "scheduled_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "end_time": (datetime.now() + timedelta(days=1, hours=1)).isoformat(),
        "notes": "First time visitor"
    }

    try:
        # Create appointment
        response = requests.post(f"{API_BASE}/appointments/", json=appointment_data)
        print(f"Create appointment: {response.status_code}")

        if response.status_code == 200:
            appointment = response.json()
            print(f"Created appointment ID: {appointment['id']}")

            # List appointments
            response = requests.get(f"{API_BASE}/appointments/")
            print(f"List appointments: {response.status_code}")

            # Cancel appointment
            response = requests.patch(f"{API_BASE}/appointments/{appointment['id']}/cancel")
            print(f"Cancel appointment: {response.status_code}")

            if response.status_code == 200:
                cancelled = response.json()
                print(f"Cancelled at: {cancelled['cancelled_at']}")
                return True

    except Exception as e:
        print(f"Test failed: {e}")
        return False

    return True

if __name__ == "__main__":
    test_appointment_flow()
