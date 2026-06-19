from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Team
from schemas import TeamCreate
from oauth2 import get_current_admin

router = APIRouter(prefix="/teams", tags=["Teams"])


# CREATE TEAM (ADMIN ONLY)
@router.post("/")
def create_team(
    team: TeamCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    new_team = Team(
        team_name=team.team_name,
        sport_id=team.sport_id,
        country=team.country,
        team_logo=team.team_logo
    )

    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    return new_team


# GET ALL TEAMS
@router.get("/")
def get_teams(db: Session = Depends(get_db)):

    return db.query(Team).all()