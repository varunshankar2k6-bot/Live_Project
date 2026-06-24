from pydantic import BaseModel, EmailStr
from typing import Optional
#USer
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: str
    phone_number: str
    gender: str
    address: str
    city: str
    state: str
    country: str
    pincode: str
class UserLogin(BaseModel):
    email: EmailStr
    password: str
#Admin
class AdminLogin(BaseModel):
    email: EmailStr
    password: str
#Sports and tournaments-
class SportCreate(BaseModel):
    sport_name: str
class TournamentCreate(BaseModel):
    tournament_name: str
    sport_id: str   # UUID used
class TeamCreate(BaseModel):
    team_name: str
    sport_id: str   # UUID used
    country: Optional[str] = None
    team_logo: Optional[str] = None
class MatchCreate(BaseModel):
    tournament_id: str   # UUID
    team1_id: str        # UUID
    team2_id: str        # UUID
    match_date: str
    status: Optional[str] = "Upcoming"
#Questions
class QuestionCreate(BaseModel):
    match_id: str       # UUID used
    question_text: str
    option1: str
    option2: str
    option3: str
    option4: str
    start_time: str
    end_time: str
    correct_answer: str
class AnswerQuestion(BaseModel):
    selected_option: str
#Response
class StandardResponse(BaseModel):
    status: str
    response: str
    data: Optional[dict] = None