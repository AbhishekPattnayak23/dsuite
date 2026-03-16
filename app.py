import sqlite3
import os
import random
import string
from datetime import datetime, date, timedelta
from functools import wraps
from flask import (Flask, render_template, redirect, url_for,
                   flash, request, session, g)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'passport-secret-key-2024'
DB_PATH = os.path.join(os.path.dirname(__file__), 'passport.db')

# ─── DB helpers ────────────────────────────────────────────────────────────────

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop('db', None)
    if db:
        db.close()


def init_db():
    db = sqlite3.connect(DB_PATH)
    db.row_factory = sqlite3.Row
    db.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        user_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        name     TEXT NOT NULL,
        email    TEXT UNIQUE NOT NULL,
        mobile   TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS slots (
        slot_id  INTEGER PRIMARY KEY AUTOINCREMENT,
        date     TEXT NOT NULL,
        time     TEXT NOT NULL,
        location TEXT NOT NULL,
        status   TEXT DEFAULT 'Available'
    );

    CREATE TABLE IF NOT EXISTS appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id        INTEGER NOT NULL REFERENCES users(user_id),
        slot_id        INTEGER NOT NULL REFERENCES slots(slot_id),
        booking_date   TEXT NOT NULL,
        booking_ref    TEXT UNIQUE NOT NULL
    );
    """)
    db.commit()

    admin = db.execute("SELECT * FROM users WHERE is_admin=1").fetchone()
    if not admin:
        db.execute(
            "INSERT INTO users (name, email, mobile, password, is_admin) VALUES (?,?,?,?,1)",
            ('Admin', 'admin@passport.gov', '9999999999',
             generate_password_hash('admin123'))
        )
        locations = ['New Delhi Office', 'Mumbai Office', 'Chennai Office']
        times     = ['09:00 AM', '10:00 AM', '11:00 AM', '02:00 PM', '03:00 PM']
        base = date.today()
        for i in range(1, 15):
            for loc in locations:
                for t in times:
                    db.execute(
                        "INSERT INTO slots (date, time, location) VALUES (?,?,?)",
                        ((base + timedelta(days=i)).isoformat(), t, loc)
                    )
        db.commit()
        print("✓ DB seeded.  Admin login: admin@passport.gov / admin123")
    db.close()


# ─── Decorators ────────────────────────────────────────────────────────────────

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated


def gen_ref():
    return 'PA' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


def email_log(user, appt, slot):
    """Simulates sending an email — prints to console."""
    print(f"""
    ── EMAIL CONFIRMATION ─────────────────────────────────
    To      : {user['email']}
    Subject : Passport Appointment Confirmed – {appt['booking_ref']}

    Dear {user['name']},

    Your appointment has been successfully booked.

    Reference : {appt['booking_ref']}
    Date      : {slot['date']}
    Time      : {slot['time']}
    Location  : {slot['location']}
    Booked On : {appt['booking_date']}

    Please arrive 10 minutes early with all required documents.

    Regards,
    Passport Office
    ───────────────────────────────────────────────────────
    """)


# ─── Auth routes ───────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name    = request.form['name'].strip()
        email   = request.form['email'].strip().lower()
        mobile  = request.form['mobile'].strip()
        pw      = request.form['password']
        confirm = request.form['confirm_password']

        if pw != confirm:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        db = get_db()
        if db.execute("SELECT 1 FROM users WHERE email=?", (email,)).fetchone():
            flash('Email already registered.', 'danger')
            return render_template('register.html')

        db.execute(
            "INSERT INTO users (name, email, mobile, password) VALUES (?,?,?,?)",
            (name, email, mobile, generate_password_hash(pw))
        )
        db.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        pw    = request.form['password']
        db    = get_db()
        user  = db.execute("SELECT * FROM users WHERE email=?", (email,)).fetchone()

        if user and check_password_hash(user['password'], pw):
            session['user_id']  = user['user_id']
            session['name']     = user['name']
            session['is_admin'] = bool(user['is_admin'])
            flash(f"Welcome, {user['name']}!", 'success')
            return redirect(url_for('admin_dashboard') if user['is_admin'] else url_for('dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# ─── User routes ───────────────────────────────────────────────────────────────

@app.route('/dashboard')
@login_required
def dashboard():
    db   = get_db()
    user = db.execute("SELECT * FROM users WHERE user_id=?", (session['user_id'],)).fetchone()
    appointments = db.execute("""
        SELECT a.appointment_id, a.booking_ref, a.booking_date,
               s.date, s.time, s.location
        FROM appointments a
        JOIN slots s ON a.slot_id = s.slot_id
        WHERE a.user_id = ?
        ORDER BY s.date DESC
    """, (session['user_id'],)).fetchall()
    today = date.today().isoformat()
    return render_template('dashboard.html', user=user, appointments=appointments, today=today)


@app.route('/slots')
@login_required
def view_slots():
    db = get_db()
    search_location = request.args.get('location', '').strip()
    search_date     = request.args.get('date', '').strip()
    today = date.today().isoformat()

    query  = "SELECT * FROM slots WHERE status='Available' AND date >= ?"
    params = [today]

    if search_location:
        query  += " AND location LIKE ?"
        params.append(f'%{search_location}%')
    if search_date:
        query  += " AND date = ?"
        params.append(search_date)

    query += " ORDER BY date, time"
    slots     = db.execute(query, params).fetchall()
    locations = db.execute("SELECT DISTINCT location FROM slots ORDER BY location").fetchall()

    return render_template('slots.html', slots=slots, locations=locations,
                           search_location=search_location, search_date=search_date)


@app.route('/book/<int:slot_id>', methods=['GET', 'POST'])
@login_required
def book(slot_id):
    db   = get_db()
    slot = db.execute("SELECT * FROM slots WHERE slot_id=?", (slot_id,)).fetchone()
    if not slot:
        flash('Slot not found.', 'danger')
        return redirect(url_for('view_slots'))

    user = db.execute("SELECT * FROM users WHERE user_id=?", (session['user_id'],)).fetchone()

    existing = db.execute(
        "SELECT 1 FROM appointments WHERE user_id=? AND slot_id=?",
        (user['user_id'], slot_id)
    ).fetchone()
    if existing:
        flash('You have already booked this slot.', 'warning')
        return redirect(url_for('view_slots'))

    if slot['status'] != 'Available':
        flash('This slot is no longer available.', 'danger')
        return redirect(url_for('view_slots'))

    if request.method == 'POST':
        ref = gen_ref()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        db.execute(
            "INSERT INTO appointments (user_id, slot_id, booking_date, booking_ref) VALUES (?,?,?,?)",
            (user['user_id'], slot_id, now, ref)
        )
        db.execute("UPDATE slots SET status='Booked' WHERE slot_id=?", (slot_id,))
        db.commit()
        appt = db.execute("SELECT * FROM appointments WHERE booking_ref=?", (ref,)).fetchone()
        email_log(user, appt, slot)
        flash(f'Appointment booked! Reference: {ref}', 'success')
        return redirect(url_for('dashboard'))

    return render_template('book_confirm.html', slot=slot, user=user)


# ─── Admin routes ──────────────────────────────────────────────────────────────

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    db = get_db()
    total_users     = db.execute("SELECT COUNT(*) FROM users WHERE is_admin=0").fetchone()[0]
    total_slots     = db.execute("SELECT COUNT(*) FROM slots").fetchone()[0]
    booked_slots    = db.execute("SELECT COUNT(*) FROM slots WHERE status='Booked'").fetchone()[0]
    available_slots = db.execute("SELECT COUNT(*) FROM slots WHERE status='Available'").fetchone()[0]
    recent = db.execute("""
        SELECT a.booking_ref, a.booking_date,
               u.name, u.email,
               s.date, s.time, s.location
        FROM appointments a
        JOIN users u ON a.user_id = u.user_id
        JOIN slots s ON a.slot_id = s.slot_id
        ORDER BY a.booking_date DESC LIMIT 10
    """).fetchall()
    return render_template('admin_dashboard.html',
                           total_users=total_users, total_slots=total_slots,
                           booked_slots=booked_slots, available_slots=available_slots,
                           recent_bookings=recent)


@app.route('/admin/slots', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_slots():
    db = get_db()
    if request.method == 'POST':
        try:
            db.execute(
                "INSERT INTO slots (date, time, location) VALUES (?,?,?)",
                (request.form['date'], request.form['time'], request.form['location'].strip())
            )
            db.commit()
            flash('Slot created successfully.', 'success')
        except Exception as e:
            flash(f'Error: {e}', 'danger')
        return redirect(url_for('admin_slots'))

    slots = db.execute("SELECT * FROM slots ORDER BY date, time").fetchall()
    return render_template('admin_slots.html', slots=slots)


@app.route('/admin/slots/delete/<int:slot_id>', methods=['POST'])
@login_required
@admin_required
def delete_slot(slot_id):
    db = get_db()
    appt = db.execute("SELECT 1 FROM appointments WHERE slot_id=?", (slot_id,)).fetchone()
    if appt:
        flash('Cannot delete a slot that has bookings.', 'danger')
    else:
        db.execute("DELETE FROM slots WHERE slot_id=?", (slot_id,))
        db.commit()
        flash('Slot deleted.', 'success')
    return redirect(url_for('admin_slots'))


@app.route('/admin/bookings')
@login_required
@admin_required
def admin_bookings():
    db = get_db()
    bookings = db.execute("""
        SELECT a.booking_ref, a.booking_date,
               u.name, u.mobile, u.email,
               s.date, s.time, s.location
        FROM appointments a
        JOIN users u ON a.user_id = u.user_id
        JOIN slots s ON a.slot_id = s.slot_id
        ORDER BY a.booking_date DESC
    """).fetchall()
    return render_template('admin_bookings.html', bookings=bookings)


# ─── Entry point ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
