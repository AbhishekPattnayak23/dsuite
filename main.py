from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from extensions import create_tables
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Appointment Booking API with cancellation support"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routers
try:
    from api.v1.appointments.router import router as appointments_router
    app.include_router(appointments_router)
    logger.info("Loaded appointments router")
except ImportError as e:
    logger.warning(f"Could not load appointments router: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    if not create_tables():
        logger.error("Failed to initialize database")
    else:
        logger.info("Application started successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "timestamp": str(__import__('datetime').datetime.utcnow()),
        "service": settings.APP_NAME
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
