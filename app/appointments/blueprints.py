"""
Appointments blueprints configuration
"""
from fastapi import APIRouter
from app.extensions import Base, engine
import logging

logger = logging.getLogger(__name__)

# Ensure blueprints handle missing extensions gracefully
class AppointmentsBlueprint:
    def __init__(self):
        self.router = APIRouter(prefix="/appointments", tags=["appointments"])

    def register_routes(self):
        """Register appointment routes"""
        @self.router.get("/")
        async def get_appointments():
            return {"appointments": [], "message": "Appointments retrieved"}

        @self.router.post("/")
        async def create_appointment():
            return {"appointment_id": 1, "message": "Appointment created"}

appointments_bp = AppointmentsBlueprint()
