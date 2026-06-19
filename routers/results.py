# routers/results.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import SessionLocal
from models import (
    Question,
    UserAnswer,
    User
)

from schemas import ResultCreate
from oauth2 import get_current_admin


router = APIRouter(prefix="/results", tags=["Results"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= DECLARE RESULT =================

@router.post("/")
def declare_result(
    res: ResultCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):

    question = db.query(Question).filter(
        Question.question_id == res.question_id
    ).first()

    question.correct_answer = res.correct_answer
    question.status = "Result Declared"

    # Get all answers
    answers = db.query(UserAnswer).filter(
        UserAnswer.question_id == res.question_id
    ).all()

    winners = []

    for ans in answers:

        user = db.query(User).filter(
            User.user_id == ans.user_id
        ).first()

        if ans.selected_option == res.correct_answer:

            ans.result = "Correct"
            user.points += 200

            winners.append(user.username)

        else:
            ans.result = "Wrong"

    db.commit()

    return {
        "message": "Result declared",
        "winners": winners
    }