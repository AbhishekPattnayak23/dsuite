from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
import logging

from auth.utils.jwt import JWTUtil
from db.session import get_db
from auth.models.user import User

security = HTTPBearer()
logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def get_current_user(self, credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
        """Get current user from JWT token"""
        try:
            token = credentials.credentials
            payload = JWTUtil.verify_token(token, "access")

            if not payload:
                raise HTTPException(status_code=401, detail="Invalid or expired token")

            user_id = payload.get("sub")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            user = self.db.query(User).filter(User.id == user_id).first()
            if not user or not user.is_active:
                raise HTTPException(status_code=401, detail="User not found or inactive")

            return user

        except Exception as e:
            logger.error(f"Auth middleware error: {str(e)}")
            raise HTTPException(status_code=401, detail=str(e))

    def get_optional_user(self, request: Request) -> Optional[User]:
        """Get user without requiring authentication"""
        auth_header = request.headers.get("authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        try:
            token = auth_header.split(" ")[1]
            payload = JWTUtil.verify_token(token, "access")

            if not payload:
                return None

            user_id = payload.get("sub")
            if not user_id:
                return None

            return self.db.query(User).filter(User.id == user_id).first()
        except:
            return None

def get_current_user(db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.get_current_user

def get_optional_user(request: Request, db: Session = Depends(get_db)):
    auth_service = AuthService(db)
    return auth_service.get_optional_user(db)
