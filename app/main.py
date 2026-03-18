"""
Main FastAPI application with graceful error handling
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Agent Integration API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import routes with error handling
try:
    from app.auth.routes import router as auth_router
    app.include_router(auth_router)
    logger.info("Auth routes loaded successfully")
except Exception as e:
    logger.warning(f"Could not load auth routes: {e}")

try:
    from app.appointments.routes import router as appointments_router
    app.include_router(appointments_router)
    logger.info("Appointments routes loaded successfully")
except Exception as e:
    logger.warning(f"Could not load appointments routes: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Agent Integration API", "version": "1.0.0"}
