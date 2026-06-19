from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Tournament
from schemas import TournamentCreate
from oauth2 import get_current_admin

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])


# CREATE TOURNAMENT (ADMIN ONLY)
@router.post("/")
def create_tournament(
    tournament: TournamentCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    new_tournament = Tournament(
        tournament_name=tournament.tournament_name,
        sport_id=tournament.sport_id
    )

    db.add(new_tournament)
    db.commit()
    db.refresh(new_tournament)

    return new_tournament


# GET ALL TOURNAMENTS
@router.get("/")
def get_tournaments(db: Session = Depends(get_db)):

    return db.query(Tournament).all()