from fastapi import FastAPI

from database import engine, Base, SessionLocal

from models import Admin

from routers import users
from routers import admin
from routers import questions
from routers import sports, tournaments, teams

app.include_router(sports.router)
app.include_router(tournaments.router)
app.include_router(teams.router)
from utils import hash_password

app = FastAPI()

# Create all tables
Base.metadata.create_all(bind=engine)


# Create predefined admin
db = SessionLocal()

existing_admin = db.query(Admin).filter(
    Admin.email == "admin@gmail.com"
).first()

if existing_admin is None:

    new_admin = Admin(

        username="admin",

        email="admin@gmail.com",

        password=hash_password(
            "admin123"
        )

    )

    db.add(new_admin)

    db.commit()

db.close()


# Include routers
app.include_router(users.router)

app.include_router(admin.router)

app.include_router(questions.router)


@app.get("/")
def home():

    return {

        "message": "Sports Prediction App Running"

    }