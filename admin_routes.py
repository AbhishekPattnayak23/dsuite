from __future__ import annotations
import logging
from flask import Blueprint, jsonify
from models import db, Appointment, Slot
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/analytics', methods=['GET'])
def analytics():
    """Get admin analytics."""
    try:
        total_bookings = Appointment.query.count()
        available_slots = Slot.query.count()
        booked_ratio = total_bookings / max(available_slots, 1)

        daily = db.session.query(
            db.func.date(Appointment.booked_at).label('date'),
            db.func.count(Appointment.id).label('count')
        ).group_by('date').all()

        return jsonify({
            'total_bookings': total_bookings,
            'available_slots': available_slots,
            'booked_ratio': booked_ratio,
            'daily': [{'date': str(d[0]), 'count': d[1]} for d in daily]
        })
    except Exception as e:
        logging.error(f"Analytics error: {e}")
        return jsonify({'error': 'Failed to fetch analytics'}), 500
