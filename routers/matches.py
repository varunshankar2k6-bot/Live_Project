from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Match
from schemas import MatchCreate
from oauth2 import get_current_admin
import logging
import uuid
router = APIRouter(prefix="/matches", tags=["Matches"])
logger = logging.getLogger(__name__)
db: Session = Depends(get_db)
#Getting admin details
@router.post("/")
def create_match(
    match: MatchCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        new_match = Match(
            tournament_id=match.tournament_id,
            team1_id=match.team1_id,
            team2_id=match.team2_id,
            match_date=match.match_date,
            status="Upcoming"
        )
        db.add(new_match)
        db.commit()
        db.refresh(new_match)
        return {
            "status": "success",
            "response": "Match created",
            "data": {"match_id": new_match.match_id}
        }
#Exception handling
    except Exception:
        logger.error("Match creation failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Match creation failed")

@router.get("/")
def get_matches(db: Session = Depends(get_db)):
    try:
        data = db.query(Match).all()

        return {
            "status": "success",
            "response": "Matches fetched",
            "data": data
        }
    except Exception:
        logger.error("Get matches failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Fetch failed")
#Match details
@router.get("/{match_id}")
def get_match(match_id: str, db: Session = Depends(get_db)):
    try:
        match = db.query(Match).filter(Match.match_id == match_id).first()
        if not match:
            raise HTTPException(status_code=404, detail="Match not found")
        return {
            "status": "success",
            "response": "Match fetched",
            "data": match
        }
    #Exception handling
    except HTTPException:
        raise
    except Exception:
        logger.error("Get match failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Match fetch error")