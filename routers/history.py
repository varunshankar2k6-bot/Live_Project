from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import History
import logging

router = APIRouter(prefix="/history", tags=["History"])
logger = logging.getLogger(__name__)
#Getting database
db: Session = Depends(get_db)
#Getting user details
@router.get("/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    try:
        data = db.query(History).filter(History.user_id == user_id).all()
        return {
            "status": "success",
            "response": "History fetched",
            "data": data
        }
    except Exception:
        logger.error("History error", exc_info=True)
        raise HTTPException(status_code=500, detail="History error")