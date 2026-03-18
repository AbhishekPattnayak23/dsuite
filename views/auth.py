from flask import Blueprint, render_template, request, jsonify, session
from werkzeug.security import check_password_hash
import secrets
from datetime import datetime, timedelta
from ..models.user import User, Session as UserSession

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    data = request.get_json()
    if not data:
        return jsonify({"error": "invalid request"}), 400

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "username and password required"}), 400

    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    # Create session
    session_token = secrets.token_hex(32)
    expires_at = datetime.utcnow() + timedelta(hours=24)

    user_session = UserSession(
        token=session_token,
        user_id=user.id,
        expires_at=expires_at
    )
    from app import db
    db.session.add(user_session)
    db.session.commit()

    session['token'] = session_token

    return jsonify({
        "session_token": session_token,
        "expires_at": expires_at.isoformat()
    })
