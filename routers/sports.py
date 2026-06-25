from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Sport
from schemas import SportCreate
from oauth2 import get_current_admin
import logging

router = APIRouter(prefix="/sports", tags=["Sports"])
logger = logging.getLogger(__name__)
from database import get_db


# Sport creation
@router.post("/")
def create_sport(
    sport: SportCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)
):
    try:
        new_sport = Sport(sport_name=sport.sport_name)
        db.add(new_sport)
        db.commit()
        db.refresh(new_sport)
        return {
            "status": "success",
            "response": "Sport created",
            "data": {"sport_id": new_sport.sport_id},
        }
    except Exception:
        logger.error("Create sport failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Sport creation failed")


# Displaying sport details
@router.get("/")
def get_sports(db: Session = Depends(get_db)):
    try:
        sports = db.query(Sport).all()

        return {"status": "success", "response": "Sports fetched", "data": sports}
    except Exception:
        logger.error("Get sports failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Fetch failed")
