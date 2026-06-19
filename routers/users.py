# routers/users.py

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from database import SessionLocal

from models import User

from schemas import UserCreate
from schemas import UserLogin

from utils import hash_password
from utils import verify_password

from jwt_utils import create_access_token


router = APIRouter()


# Database Dependency
def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()


# ================= SIGNUP =================

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
            detail="Email already exists"
        )

    new_user = User(

        username=user.username,

        email=user.email,

        password=hash_password(
            user.password
        ),

        full_name=user.full_name,

        phone_number=user.phone_number,

        gender=user.gender,

        address=user.address,

        city=user.city,

        state=user.state,

        country=user.country,

        pincode=user.pincode,

        points=500

    )

    db.add(new_user)

    db.commit()

    return {

        "message": "User created successfully"

    }


# ================= LOGIN =================

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

    if not verify_password(
            user.password,
            db_user.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )

    access_token = create_access_token(

        {
            "user_id": db_user.user_id,
            "email": db_user.email,
            "role": "user"
        }

    )

    return {

        "access_token": access_token,

        "token_type": "bearer"

    }