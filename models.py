from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base

#ALl tables created
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    phone_number = Column(String(20))
    gender = Column(String(20))
    address = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    country = Column(String(100))
    pincode = Column(String(20))
    points = Column(Integer, default=500)
    # Used for one-device login
    device_token = Column(String(255), nullable=True)
    verification_otp = Column(String(10))
    is_verified = Column(String(10), default="False")

class Admin(Base):
    __tablename__ = "admins"
    admin_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(255))

class Sport(Base):
    __tablename__ = "sports"
    sport_id = Column(Integer, primary_key=True, index=True)
    sport_name = Column(String(100), unique=True)

class Tournament(Base):
    __tablename__ = "tournaments"
    tournament_id = Column(Integer, primary_key=True, index=True)
    sport_id = Column(
        Integer,
        ForeignKey("sports.sport_id")
    )
    tournament_name = Column(String(100), nullable=False)

class Team(Base):
    __tablename__ = "teams"
    team_id = Column(Integer, primary_key=True, index=True)
    team_name = Column(String(100), nullable=False)
    sport_id = Column(
        Integer,
        ForeignKey("sports.sport_id")
    )
    country = Column(String(100))
    team_logo = Column(String(255))

class Match(Base):
    __tablename__ = "matches"
    match_id = Column(Integer, primary_key=True, index=True)
    tournament_id = Column(
        Integer,
        ForeignKey("tournaments.tournament_id")
    )
    team1_id = Column(
        Integer,
        ForeignKey("teams.team_id")
    )
    team2_id = Column(
        Integer,
        ForeignKey("teams.team_id")
    )
    match_date = Column(DateTime)
    status = Column(String(50))

class Question(Base):
    __tablename__ = "questions"
    question_id = Column(Integer, primary_key=True, index=True)
    match_id = Column(
        Integer,
        ForeignKey("matches.match_id")
    )
    admin_id = Column(
        Integer,
        ForeignKey("admins.admin_id")
    )
    question_text = Column(String(500), nullable=False)
    option1 = Column(String(100))
    option2 = Column(String(100))
    option3 = Column(String(100))
    option4 = Column(String(100))
    correct_answer = Column(String(100))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String(50))

class UserAnswer(Base):
    __tablename__ = "user_answers"
    answer_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.question_id")
    )
    selected_option = Column(String(100))
    answered_at = Column(DateTime)
    result = Column(String(50))

class Leaderboard(Base):
    __tablename__ = "leaderboard"
    leaderboard_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )
    total_points = Column(Integer)

class History(Base):
    __tablename__ = "history"
    history_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )
    question_id = Column(
        Integer,
        ForeignKey("questions.question_id")
    )
    selected_option = Column(String(100))
    correct_answer = Column(String(100))
    result = Column(String(50))
    points_change = Column(Integer)

class Notification(Base):
    __tablename__ = "notifications"
    notification_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id")
    )
    title = Column(String(255))
    message = Column(String(500))
    is_read = Column(String(10))
    created_at = Column(DateTime)