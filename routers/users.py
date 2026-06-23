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
router = APIRouter(
    tags=["Users"]
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#User signup
@router.post("/signup")
async def signup(
    user: UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )
    # Generate 6-digit OTP
    otp = str(
        random.randint(
            100000,
            999999
        )
    )
    new_user = User(
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
        verification_otp=otp,
        is_verified="False"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    # Send OTP email
    background_tasks.add_task(
        send_verification_email,
        user.email,
        otp
    )
    return {
        "message": "Verification email sent"
    }
#Verifying using OTP
@router.post("/verify")
def verify_email(
    verify: VerifyOTP,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == verify.email
    ).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if user.verification_otp != verify.otp:
        raise HTTPException(
            status_code=400,
            detail="Invalid OTP"
        )
    user.is_verified = "True"
    db.commit()
    return {
        "message": "Email verified successfully"
    }
#Login
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if db_user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    if db_user.is_verified != "True":
        raise HTTPException(
            status_code=401,
            detail="Please verify your email first"
        )
    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )
    # Allow login from only one device
    if db_user.device_token:
        raise HTTPException(
            status_code=403,
            detail="User already logged in from another device"
        )
    new_device_token = str(uuid.uuid4())
    db_user.device_token = new_device_token
    db.commit()
    access_token = create_access_token(
        {
            "user_id": db_user.user_id
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "device_token": new_device_token
    }
#Logout User
@router.post("/logout")
def logout(
    email: str,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == email
    ).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    user.device_token = None
    db.commit()
    return {
        "message": "Logged out successfully"
    }
#Getting user details
@router.get("/profile/{user_id}")
def profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.user_id == user_id
    ).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )
    return user