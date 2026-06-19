# routers/questions.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models import Question, Admin

from schemas import QuestionCreate
from oauth2 import get_current_admin


router = APIRouter(prefix="/questions", tags=["Questions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ================= CREATE QUESTION (ADMIN ONLY) =================

@router.post("/")
def create_question(
    qn: QuestionCreate,
    db: Session = Depends(get_db),
    admin: Admin = Depends(get_current_admin)
):

    if qn.start_time >= qn.end_time:
        raise HTTPException(
            status_code=400,
            detail="Invalid time range"
        )

    new_qn = Question(
        match_id=qn.match_id,
        admin_id=admin.admin_id,
        question_text=qn.question_text,
        option1=qn.option1,
        option2=qn.option2,
        option3=qn.option3,
        option4=qn.option4,
        start_time=qn.start_time,
        end_time=qn.end_time,
        status="Active"
    )

    db.add(new_qn)
    db.commit()
    db.refresh(new_qn)

    return new_qn


# ================= GET ACTIVE QUESTIONS =================

@router.get("/active")
def get_active_questions(db: Session = Depends(get_db)):

    now = datetime.utcnow()

    questions = db.query(Question).filter(
        Question.start_time <= now,
        Question.end_time >= now,
        Question.status == "Active"
    ).all()

    return questions