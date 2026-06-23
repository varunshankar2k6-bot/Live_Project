from pydantic import BaseModel, EmailStr
#Defining all classes
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

class VerifyOTP(BaseModel):
    email: EmailStr
    otp: str

class AdminLogin(BaseModel):
    email: EmailStr
    password: str

class SportCreate(BaseModel):
    sport_name: str

class TournamentCreate(BaseModel):
    tournament_name: str
    sport_id: int

class TeamCreate(BaseModel):
    team_name: str
    sport_id: int
    country: str
    team_logo: str

class MatchCreate(BaseModel):
    tournament_id: int
    team1_id: int
    team2_id: int
    match_date: str
    status: str

class QuestionCreate(BaseModel):
    match_id: int
    question_text: str
    option1: str
    option2: str
    option3: str
    option4: str
    start_time: str
    end_time: str

class AnswerQuestion(BaseModel):
    selected_option: str