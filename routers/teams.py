from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Team
from schemas import TeamCreate
from oauth2 import get_current_admin
import logging

router = APIRouter(prefix="/teams", tags=["Teams"])
logger = logging.getLogger(__name__)
db: Session = Depends(get_db)
#Creating new teams
@router.post("/")
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    try:
        new_team = Team(
            team_name=team.team_name,
            sport_id=team.sport_id,
            country=team.country,
            team_logo=team.team_logo
        )
        db.add(new_team)
        db.commit()
        db.refresh(new_team)
        return {
            "status": "success",
            "response": "Team created",
            "data": {"team_id": new_team.team_id}
        }
    except Exception:
        logger.error("Create team failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Team creation failed")
@router.get("/")
def get_teams(db: Session = Depends(get_db)):
    try:
        data = db.query(Team).all()

        return {
            "status": "success",
            "response": "Teams fetched",
            "data": data
        }
    except Exception:
        logger.error("Get teams failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Fetch failed")