from flask import session
from ..models.user import Session as UserSession, User
from datetime import datetime

def get_current_user():
    """Get current user from session token"""
    session_token = session.get('token')
    if not session_token:
        return None

    user_session = UserSession.query.filter_by(token=session_token).first()
    if not user_session or user_session.expires_at < datetime.utcnow():
        return None

    return User.query.get(user_session.user_id)
