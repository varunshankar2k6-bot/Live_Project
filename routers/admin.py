from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Admin
from utils import verify_password
from jwt_utils import create_access_token
import logging
router = APIRouter(prefix="/admin", tags=["Admin"])
logger = logging.getLogger(__name__)
#Get databse
db: Session = Depends(get_db)
#Logging in for admin using authorization
@router.post("/login")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        admin = db.query(Admin).filter(Admin.email == form_data.username).first()
        if not admin:
            raise HTTPException(status_code=404, detail="Admin not found")
        if not verify_password(form_data.password, admin.password):
            raise HTTPException(status_code=401, detail="Wrong password")
        token = create_access_token({"admin_id": admin.admin_id})
        return {
            "status": "success",
            "access_token": token,
            "user_details": {
                "admin_id": admin.admin_id,
                "email": admin.email
            }
        }
    #Error handling
    except HTTPException:
        raise
    except Exception:
        logger.error("Admin login failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Admin login error")