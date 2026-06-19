from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    username = Column(String(100), nullable=False)

    email = Column(String(100), unique=True, nullable=False)

    password = Column(String(255), nullable=False)

    full_name = Column(String(100))

    phone_number = Column(String(15))

    gender = Column(String(10))

    date_of_birth = Column(String(20))

    address = Column(String(255))

    city = Column(String(100))

    state = Column(String(100))

    country = Column(String(100))

    pincode = Column(String(10))

    points = Column(Integer, default=500)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )