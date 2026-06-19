from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from schemas import UserCreate, UserLogin
from utils import hash_password, verify_password
from auth import create_access_token
router = APIRouter(
    tags=["Users"]
)

#Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#User signup
@router.post("/signup")
def signup(
    user: UserCreate,
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
    hashed_pw = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_pw,
        full_name=user.full_name,
        phone_number=user.phone_number,
        gender=user.gender,
        date_of_birth=user.date_of_birth,
        address=user.address,
        city=user.city,
        state=user.state,
        country=user.country,
        pincode=user.pincode
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {
        "message": "User created successfully",
        "user_id": new_user.user_id
    }

#User login
@router.post("/login")
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()
    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )
    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )
    access_token = create_access_token(
        data={
            "user_id": db_user.user_id
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }