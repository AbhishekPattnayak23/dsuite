"""
Appointments API routes
"""
from fastapi import APIRouter
from app.appointments.blueprints import appointments_bp

router = appointments_bp.router

# Register routes
appointments_bp.register_routes()
