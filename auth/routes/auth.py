from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
import logging

from auth.models.user import User, PasswordResetToken
from auth.schemas import UserCreate, UserResponse, UserLogin, TokenResponse, \
    PasswordResetRequest, PasswordResetConfirm, RefreshToken
from auth.utils.password import PasswordUtil
from auth.utils.jwt import JWTUtil
from db.session import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Register a new user"""
    try:
        # Check if user exists
        existing_user = db.query(User).filter(
            or_(User.email == user_data.email)
        ).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        # Hash password
        hashed_password = PasswordUtil.hash_password(user_data.password)

        # Create user
        user = User(
            email=user_data.email,
            hashed_password=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        # Send verification email (implement email service)
        # background_tasks.add_task(send_verification_email, user.email)

        return user

    except Exception as e:
        db.rollback()
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """User login with email and password"""
    try:
        user = db.query(User).filter(User.email == form_data.username).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Check account lockout
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(
                status_code=401,
                detail=f"Account locked until {user.locked_until.strftime('%Y-%m-%d %H:%M:%S')} UTC"
            )

        # Verify password
        is_valid, needs_rehash = PasswordUtil.verify_password(
            form_data.password, user.hashed_password
        )

        if not is_valid:
            # Handle failed login attempt
            failed_attempts = int(user.failed_login_attempts or 0) + 1
            user.failed_login_attempts = str(failed_attempts)

            if failed_attempts >= 5:
                user.locked_until = datetime.utcnow() + timedelta(minutes=15)

            db.commit()
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Reset failed attempts on successful login
        user.failed_login_attempts = "0"
        user.locked_until = None
        user.last_login = datetime.utcnow()

        # Rehash if needed
        if needs_rehash:
            user.hashed_password = PasswordUtil.hash_password(form_data.password)

        # Create tokens
        access_token = JWTUtil.create_access_token({"sub": str(user.id)})
        refresh_token = JWTUtil.create_refresh_token(str(user.id))

        # Store refresh token
        user.refresh_token = refresh_token
        user.refresh_token_expires_at = datetime.utcnow() + timedelta(days=7)

        db.commit()

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=30 * 60  # 30 minutes
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Login failed")

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(token: RefreshToken, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        payload = JWTUtil.verify_token(token.refresh_token, "refresh")

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        user_id = payload.get("sub")
        user = db.query(User).filter(
            User.id == user_id,
            User.refresh_token == token.refresh_token,
            User.refresh_token_expires_at > datetime.utcnow()
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        # Create new tokens
        new_access_token = JWTUtil.create_access_token({"sub": str(user.id)})
        new_refresh_token = JWTUtil.create_refresh_token(str(user.id))

        # Update refresh token
        user.refresh_token = new_refresh_token
        user.refresh_token_expires_at = datetime.utcnow() + timedelta(days=7)
        db.commit()

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            expires_in=30 * 60
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Refresh token error: {str(e)}")
        raise HTTPException(status_code=500, detail="Token refresh failed")

@router.post("/logout")
async def logout(current_user: dict = Depends(), db: Session = Depends(get_db)):
    """Logout user and invalidate refresh token"""
    try:
        user = db.query(User).filter(User.id == current_user.get("sub")).first()
        if user:
            user.refresh_token = None
            user.refresh_token_expires_at = None
            db.commit()

        return {"message": "Logged out successfully"}

    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        raise HTTPException(status_code=500, detail="Logout failed")

@router.post("/password-reset")
async def request_password_reset(
    reset_request: PasswordResetRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """Request password reset token via email"""
    try:
        user = db.query(User).filter(User.email == reset_request.email).first()

        if not user:
            # Don't reveal if user exists
            return {"message": "If an account exists, a reset email will be sent"}

        # Generate reset token
        reset_token = PasswordUtil.generate_secure_token(32)

        # Store token
        token_record = PasswordResetToken(
            user_id=user.id,
            token=reset_token,
            expires_at=datetime.utcnow() + timedelta(hours=1)
        )

        db.add(token_record)
        db.commit()

        # Send reset email (implement email service)
        # background_tasks.add_task(send_reset_email, user.email, reset_token)

        return {"message": "If an account exists, a reset email will be sent"}

    except Exception as e:
        db.rollback()
        logger.error(f"Password reset request error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to send reset email")

@router.post("/password-reset/confirm")
async def confirm_password_reset(reset_data: PasswordResetConfirm, db: Session = Depends(get_db)):
    """Confirm password reset and update password"""
    try:
        # Find valid token
        token_record = db.query(PasswordResetToken).filter(
            PasswordResetToken.token == reset_data.token,
            PasswordResetToken.expires_at > datetime.utcnow(),
            PasswordResetToken.used == False
        ).first()

        if not token_record:
            raise HTTPException(status_code=400, detail="Invalid or expired reset token")

        # Get user
        user = db.query(User).filter(User.id == token_record.user_id).first()
        if not user:
            raise HTTPException(status_code=400, detail="User not found")

        # Update password
        user.hashed_password = PasswordUtil.hash_password(reset_data.new_password)

        # Mark token as used
        token_record.used = True

        # Invalidate existing refresh tokens
        user.refresh_token = None
        user.refresh_token_expires_at = None

        db.commit()

        return {"message": "Password reset successfully"}

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Password reset confirmation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to reset password")
