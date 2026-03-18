from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine
from app.core.config import settings
from app.models import user, slot, appointment
from app.routes import slots, auth, appointments

# Create database tables
user.Base.metadata.create_all(bind=engine)
slot.Base.metadata.create_all(bind=engine)
appointment.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Appointment Booking Service",
    version="1.0.0",
    description="Slot management and appointment booking system"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(slots.router)
app.include_router(auth.router)
app.include_router(appointments.router)

@app.get("/")
async def root():
    return {"message": "Appointment booking service is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "appointment-service"}
