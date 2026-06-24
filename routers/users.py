from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin, VerifyOTP
from utils import hash_password, verify_password
from jwt_utils import create_access_token
from email_utils import send_verification_email
import uuid
import random
import logging

router = APIRouter(tags=["Users"])
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# SIGNUP
@router.post("/signup")
def signup(user: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User).filter(User.email == user.email).first()

        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        otp = str(random.randint(100000, 999999))

        new_user = User(
            user_id=str(uuid.uuid4()),
            username=user.username,
            email=user.email,
            password=hash_password(user.password),
            full_name=user.full_name,
            phone_number=user.phone_number,
            gender=user.gender,
            address=user.address,
            city=user.city,
            state=user.state,
            country=user.country,
            pincode=user.pincode,
            points=500,
            verification_otp=otp,
            is_verified="False"
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        background_tasks.add_task(send_verification_email, user.email, otp)

        token = create_access_token({"user_id": new_user.user_id})

        return {
            "status": "success",
            "response": f"Successfully registered with username {user.username}",
            "access_token": token,
            "user_details": {
                "user_id": new_user.user_id,
                "username": new_user.username,
                "email": new_user.email,
                "points": new_user.points
            }
        }

    except HTTPException:
        raise
    except Exception:
        logger.error("Signup failed", exc_info=True)
        raise HTTPException(status_code=500, detail="User not able to register")


# VERIFY OTP
@router.post("/verify")
def verify_email(data: VerifyOTP, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == data.email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        if user.verification_otp != data.otp:
            raise HTTPException(status_code=400, detail="Invalid OTP")

        user.is_verified = "True"
        db.commit()

        return {
            "status": "success",
            "response": "Email verified successfully"
        }

    except HTTPException:
        raise
    except Exception:
        logger.error("OTP verification failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Verification failed")


# LOGIN
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if db_user.is_verified != "True":
            raise HTTPException(status_code=401, detail="Verify email first")

        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        token = create_access_token({"user_id": db_user.user_id})

        return {
            "status": "success",
            "access_token": token,
            "user_details": {
                "user_id": db_user.user_id,
                "username": db_user.username,
                "email": db_user.email,
                "points": db_user.points
            }
        }

    except HTTPException:
        raise
    except Exception:
        logger.error("Login failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed")


# LOGOUT
@router.post("/logout/{user_id}")
def logout(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.device_token = None
        db.commit()

        return {
            "status": "success",
            "response": "Logged out successfully"
        }

    except HTTPException:
        raise
    except Exception:
        logger.error("Logout failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Logout failed")


# PROFILE
@router.get("/profile/{user_id}")
def profile(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "status": "success",
            "response": "User profile fetched",
            "data": {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "points": user.points
            }
        }

    except HTTPException:
        raise
    except Exception:
        logger.error("Profile fetch failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Profile error")