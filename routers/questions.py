from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question, Admin
from schemas import QuestionCreate
from oauth2 import get_current_admin
router = APIRouter(
    prefix="/questions",
    tags=["Questions"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Creating question
@router.post("/create")
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    current_admin: Admin = Depends(get_current_admin)
):
    new_question = Question(
        match_id=question.match_id,
        admin_id=current_admin.admin_id,
        question_text=question.question_text,
        option1=question.option1,
        option2=question.option2,
        option3=question.option3,
        option4=question.option4,
        start_time=question.start_time,
        end_time=question.end_time,
        status="ACTIVE"
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return {
        "message": "Question created successfully"
    }