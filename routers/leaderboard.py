from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import User
import logging

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])
logger = logging.getLogger(__name__)
from database import get_db


# Getting leaderboard
@router.get("/")
def get_leaderboard(db: Session = Depends(get_db)):
    try:
        users = db.query(User).order_by(User.points.desc()).all()
        data = []
        rank = 1
        for u in users:
            data.append({"rank": rank, "username": u.username, "points": u.points})
            rank += 1
        return {"status": "success", "response": "Leaderboard fetched", "data": data}
    except Exception:
        logger.error("Leaderboard error", exc_info=True)
        raise HTTPException(status_code=500, detail="Leaderboard error")
