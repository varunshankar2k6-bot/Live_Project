from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime

from database import Base


# ---------------- USER ----------------

class User(Base):
    __tablename__ = "users"

    user_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    full_name = Column(
        String(100)
    )

    phone_number = Column(
        String(15)
    )

    gender = Column(
        String(10)
    )

    date_of_birth = Column(
        String(20)
    )

    address = Column(
        String(255)
    )

    city = Column(
        String(100)
    )

    state = Column(
        String(100)
    )

    country = Column(
        String(100)
    )

    pincode = Column(
        String(10)
    )

    points = Column(
        Integer,
        default=500
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )


# ---------------- ADMIN ----------------

class Admin(Base):
    __tablename__ = "admins"

    admin_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(100),
        unique=True,
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )


# ---------------- QUESTION ----------------

class Question(Base):
    __tablename__ = "questions"

    question_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    question = Column(
        String(500),
        nullable=False
    )

    option1 = Column(
        String(100),
        nullable=False
    )

    option2 = Column(
        String(100),
        nullable=False
    )

    option3 = Column(
        String(100),
        nullable=False
    )

    option4 = Column(
        String(100),
        nullable=False
    )

    correct_answer = Column(
        String(100),
        nullable=True
    )

    start_time = Column(
        DateTime
    )

    end_time = Column(
        DateTime
    )

    created_by = Column(
        Integer,
        ForeignKey("admins.admin_id")
    )