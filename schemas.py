# schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime


# ================= USER =================

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


# ================= ADMIN =================

class AdminLogin(BaseModel):

    email: EmailStr
    password: str


# ================= SPORT =================

class SportCreate(BaseModel):

    sport_name: str


# ================= TOURNAMENT =================

class TournamentCreate(BaseModel):

    tournament_name: str
    sport_id: int


# ================= TEAM =================

class TeamCreate(BaseModel):

    team_name: str
    sport_id: int
    country: str
    team_logo: str


# ================= MATCH =================

class MatchCreate(BaseModel):

    tournament_id: int
    team1_id: int
    team2_id: int
    match_date: datetime


# ================= QUESTION =================

class QuestionCreate(BaseModel):

    match_id: int

    question_text: str

    option1: str

    option2: str

    option3: str

    option4: str

    start_time: datetime

    end_time: datetime


# ================= USER ANSWER =================

class UserAnswerCreate(BaseModel):

    question_id: int

    selected_option: str


# ================= RESULT =================

class ResultCreate(BaseModel):

    question_id: int

    correct_answer: str


# ================= NOTIFICATION =================

class NotificationResponse(BaseModel):

    title: str

    message: str

    class Config:

        from_attributes = True