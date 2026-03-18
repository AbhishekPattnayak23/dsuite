from flask import Blueprint, render_template
from ..utils.session_helpers import get_current_user

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/')
def admin_dashboard():
    user = get_current_user()
    if not user or user.role != 'admin':
        return "Access Denied", 403

    return render_template('admin/dashboard.html', user=user)
