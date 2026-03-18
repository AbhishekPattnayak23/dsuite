from __future__ import annotations
import logging
import datetime
from flask import Blueprint, jsonify, request
from passlib.hash import argon2
import jwt
from models import db, User, PasswordReset

auth_bp = Blueprint('auth', __name__)
SECRET = 'jwt-secret-change-in-prod'

def generate_token(user_id):
    """Generate JWT token."""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register new user."""
    try:
        data = request.json
        username = data['username']
        email = data['email']
        password = data['password']

        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400

        user = User(
            username=username,
            email=email,
            password_hash=argon2.hash(password)
        )
        db.session.add(user)
        db.session.commit()

        token = generate_token(user.id)
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })
    except Exception as e:
        logging.error(f"Registration error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """User login."""
    try:
        data = request.json
        email = data['email']
        password = data['password']

        user = User.query.filter_by(email=email).first()
        if not user or not argon2.verify(password, user.password_hash):
            return jsonify({'error': 'Invalid credentials'}), 401

        token = generate_token(user.id)
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })
    except Exception as e:
        logging.error(f"Login error: {e}")
        return jsonify({'error': 'Login failed'}), 500
