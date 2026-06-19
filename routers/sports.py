from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Sport
from schemas import SportCreate
from oauth2 import get_current_admin

router = APIRouter(prefix="/sports", tags=["Sports"])

@router.post("/")
def create_sport(sport: SportCreate, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    new_sport = Sport(sport_name=sport.sport_name)
    db.add(new_sport)
    db.commit()
    db.refresh(new_sport)
    return new_sport

@router.get("/")
def get_sports(db: Session = Depends(get_db)):
    return db.query(Sport).all()