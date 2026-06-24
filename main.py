from fastapi import FastAPI
from database import engine, Base, SessionLocal
from models import Admin
from utils import hash_password

import routers.users as users
import routers.admin as admin
import routers.sports as sports
import routers.tournaments as tournaments
import routers.teams as teams
import routers.matches as matches
import routers.questions as questions
import routers.history as history
import routers.notifications as notifications
import routers.leaderboard as leaderboard

app = FastAPI(title="Sports Prediction App ComeonDa")
Base.metadata.create_all(bind=engine)
def create_default_admin():
    db = SessionLocal()
    try:
        existing = db.query(Admin).filter(Admin.email == "admin@gmail.com").first()
        if not existing:
            admin_user = Admin(
                username="admin",
                email="admin@gmail.com",
                password=hash_password("admin123")
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()
create_default_admin()
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(sports.router)
app.include_router(tournaments.router)
app.include_router(teams.router)
app.include_router(matches.router)
app.include_router(questions.router)
app.include_router(history.router)
app.include_router(notifications.router)
app.include_router(leaderboard.router)
@app.get("/")
def home():
    return {
        "status": "success",
        "response": "Sports Prediction App Running",
        "data": {
            "admin_email": "admin@gmail.com"
        }
    }