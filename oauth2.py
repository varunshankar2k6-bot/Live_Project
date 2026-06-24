from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import logging

from database import SessionLocal
from models import User, Admin
from jwt_utils import SECRET_KEY, ALGORITHM
logger = logging.getLogger(__name__)
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/admin/login"
)
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        logger.error("DB error in OAuth", exc_info=True)
        raise
    finally:
        db.close()
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="User authorization failed"
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
    except JWTError as e:
        logger.error("User token decode failed", exc_info=True)
        raise credentials_exception
    user = db.query(User).filter(
        User.user_id == user_id
    ).first()
    if user is None:
        raise credentials_exception
    return user
def get_current_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Admin authorization failed"
    )
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        admin_id = payload.get("admin_id")
        if admin_id is None:
            raise credentials_exception
    except JWTError:
        logger.error("Admin token decode failed", exc_info=True)
        raise credentials_exception
    admin = db.query(Admin).filter(
        Admin.admin_id == admin_id
    ).first()
    if admin is None:
        raise credentials_exception
    return admin