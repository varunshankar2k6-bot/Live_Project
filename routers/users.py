from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from schemas import UserCreate, UserLogin
from utils import hash_password, verify_password
from jwt_utils import create_access_token
import uuid
import logging

router = APIRouter(tags=["Users"])


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    try:
        existing_email = db.query(User).filter(User.email == user.email).first()

        if existing_email:
            raise HTTPException(status_code=400, detail="Email already registered")

        existing_username = (
            db.query(User).filter(User.username == user.username).first()
        )

        if existing_username:
            raise HTTPException(status_code=400, detail="Username already exists")

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
            device_token=None,
            is_verified="True",
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        token = create_access_token({"user_id": new_user.user_id})

        return {
            "status": "success",
            "response": f"Successfully registered with username {user.username}",
            "access_token": token,
            "user_details": {
                "user_id": new_user.user_id,
                "username": new_user.username,
                "email": new_user.email,
                "points": new_user.points,
            },
        }

    except HTTPException:
        raise

    except Exception:
        logging.error("User not able to register", exc_info=True)
        raise HTTPException(status_code=500, detail="User not able to register")


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.email == user.email).first()

        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        if not verify_password(user.password, db_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")

        if db_user.device_token:
            raise HTTPException(
                status_code=403, detail="User already logged in from another device"
            )

        new_device_token = str(uuid.uuid4())

        db_user.device_token = new_device_token
        db.commit()

        token = create_access_token({"user_id": db_user.user_id})

        return {
            "status": "success",
            "access_token": token,
            "user_details": {
                "user_id": db_user.user_id,
                "username": db_user.username,
                "email": db_user.email,
                "points": db_user.points,
                "device_token": new_device_token,
            },
        }

    except HTTPException:
        raise

    except Exception:
        logging.error("Login failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Login failed")


@router.post("/logout/{user_id}")
def logout(user_id: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.device_token = None

        db.commit()

        return {"status": "success", "response": "Logged out successfully"}

    except HTTPException:
        raise

    except Exception:
        logging.error("Logout failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Logout failed")


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
                "full_name": user.full_name,
                "phone_number": user.phone_number,
                "gender": user.gender,
                "address": user.address,
                "city": user.city,
                "state": user.state,
                "country": user.country,
                "pincode": user.pincode,
                "points": user.points,
            },
        }

    except HTTPException:
        raise

    except Exception:
        logging.error("Profile fetch failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Profile error")
