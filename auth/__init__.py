from fastapi import FastAPI
from auth.routes.auth import router as auth_router

def init_auth(app: FastAPI):
    """Initialize authentication module"""
    app.include_router(auth_router)
