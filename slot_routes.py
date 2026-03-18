from __future__ import annotations
import logging
from flask import Blueprint, jsonify, request
from models import db, Slot
from datetime import datetime

slot_bp = Blueprint('slot', __name__)

@slot_bp.route('/slots', methods=['GET'])
def get_slots():
    """Get available slots."""
    try:
        location = request.args.get('location')
        date = request.args.get('date')

        query = Slot.query
        if location:
            query = query.filter(Slot.location.ilike(f'%{location}%'))
        if date:
            query = query.filter(Slot.date == datetime.strptime(date, '%Y-%m-%d').date())

        slots = query.all()
        return jsonify([{
            'id': s.id,
            'location': s.location,
            'date': str(s.date),
            'capacity': s.capacity,
            'available': s.capacity - len([a for a in s.appointments])
        }])
    except Exception as e:
        logging.error(f"Get slots error: {e}")
        return jsonify({'error': 'Failed to fetch slots'}), 500

@slot_bp.route('/slots', methods=['POST'])
def create_slot():
    """Admin create slot."""
    try:
        data = request.json
        slot = Slot(
            location=data['location'],
            date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
            capacity=data['capacity']
        )
        db.session.add(slot)
        db.session.commit()
        return jsonify({'slot': {
            'id': slot.id,
            'location': slot.location,
            'date': str(slot.date),
            'capacity': slot.capacity
        }})
    except Exception as e:
        logging.error(f"Create slot error: {e}")
        return jsonify({'error': 'Failed to create slot'}), 500
