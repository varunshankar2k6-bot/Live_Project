# routers/leaderboard.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= GET LEADERBOARD =================

@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):

    users = db.query(User).order_by(User.points.desc()).all()

    leaderboard = []

    rank = 1

    for u in users:

        leaderboard.append({
            "rank": rank,
            "username": u.username,
            "points": u.points
        })

        rank += 1

    return leaderboard