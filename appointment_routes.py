from __future__ import annotations
import logging
from flask import Blueprint, jsonify, request
from models import db, Appointment, Slot
import time

appointment_bp = Blueprint('appointment', __name__)
redis_locks = {}

@appointment_bp.route('/appointments', methods=['POST'])
def book_appointment():
    """Book an appointment."""
    try:
        data = request.json
        slot_id = data['slot_id']
        user_id = 1  # Mock user ID, replace with JWT auth

        # Redis lock simulation
        lock_key = f"slot:{slot_id}"
        if lock_key in redis_locks and redis_locks[lock_key] > time.time():
            return jsonify({'error': 'Slot temporarily unavailable'}), 429

        redis_locks[lock_key] = time.time() + 5

        slot = Slot.query.get(slot_id)
        if not slot:
            return jsonify({'error': 'Slot not found'}), 404

        booked = len(slot.appointments)
        if booked >= slot.capacity:
            return jsonify({'error': 'Slot fully booked'}), 400

        appointment = Appointment(user_id=user_id, slot_id=slot_id)
        db.session.add(appointment)
        db.session.commit()

        del redis_locks[lock_key]
        return jsonify({'appointment': {
            'id': appointment.id,
            'slot_id': appointment.slot_id,
            'booked_at': str(appointment.booked_at)
        }})
    except Exception as e:
        logging.error(f"Book appointment error: {e}")
        return jsonify({'error': 'Booking failed'}), 500

@appointment_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
def cancel_appointment(appointment_id):
    """Cancel appointment."""
    try:
        appointment = Appointment.query.get(appointment_id)
        if not appointment:
            return jsonify({'error': 'Appointment not found'}), 404

        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'appointment cancelled'})
    except Exception as e:
        logging.error(f"Cancel appointment error: {e}")
        return jsonify({'error': 'Cancellation failed'}), 500

@appointment_bp.route('/appointments/me', methods=['GET'])
def my_appointments():
    """Get user appointments."""
    try:
        user_id = 1  # Mock user ID
        apps = Appointment.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'id': a.id,
            'slot': {
                'id': a.slot.id,
                'location': a.slot.location,
                'date': str(a.slot.date)
            },
            'booked_at': str(a.booked_at)
        }])
    except Exception as e:
        logging.error(f"Get appointments error: {e}")
        return jsonify({'error': 'Failed to fetch appointments'}), 500
