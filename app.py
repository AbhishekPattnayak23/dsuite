from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slots import router as slots_router
import uvicorn
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Slots API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(slots_router)

@app.on_event("startup")
async def startup_event():
    from database import init_db
    init_db()
    logger.info("Database initialized")

@app.get("/")
async def root():
    return {"message": "Slots API is running"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
