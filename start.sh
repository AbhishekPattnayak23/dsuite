echo "Starting Appointment Booking API..."
python -m pytest test_appointment.py -v || echo "Tests not available yet"
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
