from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import History
import logging

router = APIRouter(prefix="/history", tags=["History"])

logger = logging.getLogger(__name__)


@router.get("/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    try:
        data = db.query(History).filter(History.user_id == user_id).all()

        return {
            "status": "success",
            "response": "History fetched",
            "data": [
                {
                    "history_id": h.history_id,
                    "user_id": h.user_id,
                    "question_id": h.question_id,
                    "selected_option": h.selected_option,
                    "correct_answer": h.correct_answer,
                    "result": h.result,
                    "points_change": h.points_change,
                }
                for h in data
            ],
        }

    except Exception:
        logger.error("History error", exc_info=True)
        raise HTTPException(status_code=500, detail="History error")
