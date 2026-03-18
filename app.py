import os
from flask import Flask, render_template, redirect, url_for, session, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/slots')
def get_slots():
    return jsonify([
        {"id": 1, "date": "2024-01-15", "time": "09:00", "available": True},
        {"id": 2, "date": "2024-01-15", "time": "10:00", "available": True}
    ])

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})
