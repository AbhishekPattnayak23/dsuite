from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from datetime import datetime, date
from ..models.user import User, Slot, Booking
from ..utils.session_helpers import get_current_user
from sqlalchemy import and_

appointments = Blueprint('appointments', __name__)

@appointments.route('/')
def home():
    current_user = get_current_user()
    if not current_user:
        return redirect(url_for('auth.login'))

    today = date.today()
    next_week = today.replace(day=today.day + 7)

    # Get bookings for current user
    user_bookings = Booking.query.join(Slot).filter(
        and_(
            Booking.user_id == current_user.id,
            Booking.canceled == False
        )
    ).all()

    bookings_list = []
    for booking in user_bookings:
        bookings_list.append({
            'booking_id': booking.id,
            'slot_id': booking.slot_id,
            'location': booking.slot.location,
            'start_time': booking.slot.start_time.isoformat(),
            'end_time': booking.slot.end_time.isoformat()
        })

    return render_template('index.html',
                         user=current_user,
                         bookings=bookings_list)

@appointments.route('/api/slots')
def get_slots():
    """Get available slots based on location and date"""
    location = request.args.get('location')
    date_str = request.args.get('date')

    if not location or not date_str:
        return jsonify({"error": "location and date required"}), 400

    try:
        slot_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "invalid date format"}), 400

    slots = Slot.query.filter(
        and_(
            Slot.location == location,
            Slot.start_time >= datetime.combine(slot_date, datetime.min.time()),
            Slot.start_time < datetime.combine(slot_date, datetime.max.time())
        )
    ).all()

    slots_list = []
    for slot in slots:
        is_booked = Booking.query.filter(
            and_(
                Booking.slot_id == slot.id,
                Booking.canceled == False
            )
        ).first() is not None

        slots_list.append({
            'slot_id': slot.id,
            'location': slot.location,
            'start_time': slot.start_time.isoformat(),
            'end_time': slot.end_time.isoformat(),
            'is_booked': is_booked
        })

    return jsonify(slots_list)
