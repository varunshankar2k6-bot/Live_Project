from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Tournament
from schemas import TournamentCreate
from oauth2 import get_current_admin
import logging

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])
logger = logging.getLogger(__name__)
from database import get_db


# Creating new tournament
@router.post("/")
def create_tournament(
    tournament: TournamentCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    try:
        new_tournament = Tournament(
            sport_id=tournament.sport_id, tournament_name=tournament.tournament_name
        )
        db.add(new_tournament)
        db.commit()
        db.refresh(new_tournament)
        return {
            "status": "success",
            "response": "Tournament created",
            "data": {"tournament_id": new_tournament.tournament_id},
        }
    except Exception:
        logger.error("Tournament creation failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Tournament error")


# Getting details
@router.get("/")
def get_tournaments(db: Session = Depends(get_db)):
    try:
        data = db.query(Tournament).all()
        return {"status": "success", "response": "Tournaments fetched", "data": data}
    except Exception:
        logger.error("Fetch tournaments failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Fetch error")
