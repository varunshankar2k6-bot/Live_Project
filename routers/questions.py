from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import Question, User, UserAnswer, History, Leaderboard
from schemas import QuestionCreate, AnswerQuestion
from oauth2 import get_current_admin
from datetime import datetime
import logging

router = APIRouter(prefix="/questions", tags=["Questions"])
logger = logging.getLogger(__name__)

from database import get_db


# Creating question by admin authorization
@router.post("/create")
def create_question(
    question: QuestionCreate,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin),
):
    try:
        new_q = Question(
            match_id=question.match_id,
            admin_id=admin.admin_id,
            question_text=question.question_text,
            option1=question.option1,
            option2=question.option2,
            option3=question.option3,
            option4=question.option4,
            correct_answer=question.correct_answer,
            start_time=question.start_time,
            end_time=question.end_time,
            status="ACTIVE",
        )
        db.add(new_q)
        db.commit()
        db.refresh(new_q)
        return {
            "status": "success",
            "response": "Question created",
            "data": {"question_id": new_q.question_id},
        }
    # Exception Handling
    except Exception:
        logger.error("Question create failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Question error")


# Exception if repeat
@router.post("/answer/{user_id}/{question_id}")
def answer_question(
    user_id: str, question_id: str, ans: AnswerQuestion, db: Session = Depends(get_db)
):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        question = (
            db.query(Question).filter(Question.question_id == question_id).first()
        )
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")
        already = (
            db.query(UserAnswer)
            .filter(
                UserAnswer.user_id == user_id, UserAnswer.question_id == question_id
            )
            .first()
        )
        if already:
            raise HTTPException(status_code=400, detail="Already answered")
        now = datetime.utcnow()
        # Question end time
        if now < question.start_time or now > question.end_time:
            raise HTTPException(status_code=400, detail="Question not active")
        correct = ans.selected_option == question.correct_answer
        result = "Won" if correct else "Lost"
        points = 10 if correct else 0
        # Points update
        if correct:
            user.points += 10
        ua = UserAnswer(
            user_id=user_id,
            question_id=question_id,
            selected_option=ans.selected_option,
            answered_at=now,
            result=result,
        )
        db.add(ua)
        # History updation
        history = History(
            user_id=user_id,
            question_id=question_id,
            selected_option=ans.selected_option,
            correct_answer=question.correct_answer,
            result=result,
            points_change=points,
        )
        db.add(history)
        lb = db.query(Leaderboard).filter(Leaderboard.user_id == user_id).first()
        if lb:
            lb.total_points = user.points
        else:
            lb = Leaderboard(user_id=user_id, total_points=user.points)
            db.add(lb)
        db.commit()
        return {
            "status": "success",
            "response": "Answer submitted",
            "data": {
                "result": result,
                "points_added": points,
                "total_points": user.points,
            },
        }
    except HTTPException:
        raise
    except Exception:
        logger.error("Answer failed", exc_info=True)
        raise HTTPException(status_code=500, detail="Answer error")
