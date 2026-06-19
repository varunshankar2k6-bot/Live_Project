from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Admin
from schemas import AdminLogin
from utils import verify_password
from jwt_utils import create_access_token
router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)
# Database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Admin
@router.post("/login")
def admin_login(
        admin: AdminLogin,
        db: Session = Depends(get_db)
):
    db_admin = db.query(Admin).filter(
        Admin.email == admin.email
    ).first()
    if db_admin is None:
        raise HTTPException(
            status_code=404,
            detail="Admin not found"
        )
    if not verify_password(
            admin.password,
            db_admin.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect password"
        )
    access_token = create_access_token(
        {
            "admin_id": db_admin.admin_id,
            "email": db_admin.email,
            "role": "admin"
        }
    )
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }