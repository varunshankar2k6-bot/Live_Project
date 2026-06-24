from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from database import SessionLocal
from models import User, Question, UserAnswer
from schemas import UserAnswerCreate
from oauth2 import get_current_user

router = APIRouter(
    prefix="/answers",
    tags=["Answers"]
)
#Again getting database
db: Session = Depends(get_db)
#Post api for answer section
@router.post("/")
def submit_answer(
    ans: UserAnswerCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # Check if question exists
    question = db.query(Question).filter(
        Question.question_id == ans.question_id
    ).first()
    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )
    now = datetime.utcnow()
    #Setting end time and question expiry
    if now > question.end_time:
        raise HTTPException(
            status_code=400,
            detail="Question expired"
        )
    if user.points < 100:
        raise HTTPException(
            status_code=400,
            detail="Not enough points"
        )
    # Deduct points for answering
    user.points -= 100
    answer = UserAnswer(
        user_id=user.user_id,
        question_id=ans.question_id,
        selected_option=ans.selected_option,
        answered_at=now,
        result="Pending"
    )
    db.add(answer)
    db.commit()
    db.refresh(answer)
    return {
        "message": "Answer submitted",
        "deducted": 100
    }