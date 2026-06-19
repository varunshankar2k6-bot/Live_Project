from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Admin

from schemas import AdminLogin

from utils import verify_password

from auth import create_access_token


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()


@router.post("/login")
def admin_login(
        admin: AdminLogin,
        db: Session = Depends(get_db)
):

    db_admin = db.query(Admin).filter(
        Admin.email == admin.email
    ).first()

    if not db_admin:

        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
            admin.password,
            db_admin.password
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        {
            "admin_id": db_admin.admin_id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }