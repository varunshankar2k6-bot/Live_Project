from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Match
from schemas import MatchCreate
from oauth2 import get_current_admin
router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def create_match(
    match: MatchCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # New match with default status
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
        "message": "Match created successfully",
        "match": new_match
    }

@router.get("/")
def get_matches(
    db: Session = Depends(get_db)
):
    matches = db.query(Match).all()

    return matches

@router.get("/{match_id}")
def get_match(
    match_id: int,
    db: Session = Depends(get_db)
):
    match = db.query(Match).filter(
        Match.match_id == match_id
    ).first()

    if not match:
        raise HTTPException(
            status_code=404,
            detail="Match not found"
        )

    return match