from __future__ import annotations
import os
from flask import Flask, render_template
from flask_cors import CORS
from models import db, init_db
from auth_routes import auth_bp
from slot_routes import slot_bp
from appointment_routes import appointment_bp
from admin_routes import admin_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-change-in-prod')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///passport.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(slot_bp, url_prefix='/api')
app.register_blueprint(appointment_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api')

@app.route('/')
def index():
    """Serve welcome dashboard."""
    return render_template('index.html')

with app.app_context():
    init_db()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
