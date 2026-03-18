from flask import Blueprint, request, jsonify
from app.extensions import db
from app.appointments.models import Slot, Appointment
from app.appointments.services import AppointmentService
from flask_jwt_extended import jwt_required, get_jwt_identity

appointments_bp = Blueprint('appointments', __name__, url_prefix='/api')

@appointments_bp.route('/slots', methods=['GET'])
@jwt_required(optional=True)
def get_slots():
    location = request.args.get('location')
    date = request.args.get('date')

    query = db.session.query(Slot)

    if location:
        query = query.filter(Slot.location.ilike(f'%{location}%'))
    if date:
        query = query.filter(Slot.date == date)

    slots = query.all()
    return jsonify([
        {
            'id': slot.id,
            'location': slot.location,
            'date': slot.date.isoformat(),
            'capacity': slot.capacity,
            'available': slot.available
        }
        for slot in slots
    ]), 200

@appointments_bp.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    user_id = get_jwt_identity()
    slot_id = request.json.get('slot_id')

    if not slot_id:
        return jsonify({'error': 'slot_id is required'}), 400

    service = AppointmentService()
    appointment = service.book_appointment(user_id, slot_id)

    if not appointment:
        return jsonify({'error': 'Slot unavailable or already booked by user'}), 400

    return jsonify({
        'appointment': {
            'id': appointment.id,
            'slot_id': appointment.slot_id,
            'booked_at': appointment.booked_at.isoformat()
        }
    }), 201

@appointments_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def cancel_appointment(appointment_id):
    user_id = get_jwt_identity()
    appointment = Appointment.query.filter_by(id=appointment_id, user_id=user_id).first()

    if not appointment:
        return jsonify({'error': 'Appointment not found'}), 404

    db.session.delete(appointment)
    db.session.commit()

    return jsonify({'message': 'appointment cancelled'}), 200

@appointments_bp.route('/appointments/me', methods=['GET'])
@jwt_required()
def get_user_appointments():
    user_id = get_jwt_identity()
    appointments = Appointment.query.filter_by(user_id=user_id).all()

    return jsonify([
        {
            'id': appointment.id,
            'slot': {
                'id': appointment.slot.id,
                'location': appointment.slot.location,
                'date': appointment.slot.date.isoformat(),
                'capacity': appointment.slot.capacity
            },
            'booked_at': appointment.booked_at.isoformat()
        }
        for appointment in appointments
    ]), 200
