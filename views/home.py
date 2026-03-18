from flask import Blueprint, render_template, jsonify, request, session
from models import User, Slot, Booking, db
from datetime import datetime, date, timedelta
import json

home_bp = Blueprint('home', __name__, url_prefix='')

@home_bp.route('/')
def index():
    return render_template('home.html')

@home_bp.route('/api/slots')
def get_slots():
    location = request.args.get('location')
    date_str = request.args.get('date')

    query = Slot.query.filter_by(is_booked=False)

    if location:
        query = query.filter(Slot.location == location)

    if date_str:
        slot_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        start_dt = datetime.combine(slot_date, datetime.min.time())
        end_dt = datetime.combine(slot_date, datetime.max.time())
        query = query.filter(
            Slot.start_time >= start_dt,
            Slot.start_time <= end_dt
        )

    slots = query.order_by(Slot.start_time).all()

    return jsonify([{
        'slot_id': slot.id,
        'location': slot.location,
        'start_time': slot.start_time.isoformat(),
        'end_time': slot.end_time.isoformat(),
        'is_booked': slot.is_booked
    } for slot in slots])

@home_bp.route('/api/bookings/mine')
def get_my_bookings():
    token = request.cookies.get('sessionToken')
    if not token:
        return jsonify([])

    from models import Session
    sess = Session.query.filter_by(token=token, expires_at>datetime.utcnow()).first()
    if not sess:
        return jsonify([])

    bookings = Booking.query.filter_by(user_id=sess.user_id, canceled=False).join(Slot).all()

    return jsonify([{
        'booking_id': booking.id,
        'reference_code': f"{booking.id:06d}",
        'location': booking.slot.location,
        'date': booking.slot.start_time.strftime('%Y-%m-%d'),
        'time': booking.slot.start_time.strftime('%H:%M')
    } for booking in bookings])

@home_bp.route('/api/user/status')
def user_status():
    token = request.cookies.get('sessionToken')
    if not token:
        return jsonify({'logged_in': False})

    from models import Session
    sess = Session.query.filter_by(token=token, expires_at>datetime.utcnow()).first()
    if not sess:
        return jsonify({'logged_in': False})

    user = User.query.get(sess.user_id)
    return jsonify({
        'logged_in': True,
        'username': user.username,
        'is_admin': user.role == 'admin'
    })
