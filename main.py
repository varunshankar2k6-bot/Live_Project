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

app = FastAPI(
    title="Sports Prediction App ComeonDa"
)
Base.metadata.create_all(
    bind=engine
)
db = SessionLocal()
existing_admin = db.query(
    Admin
).filter(
    Admin.email == "admin@gmail.com"
).first()

# Create default admin if it doesn't exist
if existing_admin is None:
    admin_user = Admin(
        username="admin",
        email="admin@gmail.com",
        password=hash_password(
            "admin123"
        )
    )
    db.add(admin_user)
    db.commit()
db.close()

app.include_router(users.router)
app.include_router(admin.router)
app.include_router(sports.router)
app.include_router(tournaments.router)
app.include_router(teams.router)
app.include_router(matches.router)
app.include_router(questions.router)
app.include_router(history.router)
app.include_router(notifications.router)

@app.get("/")
def home():
    return {
        "message": "Sports Prediction App Running",
        "admin_email": "admin@gmail.com",
        "admin_password": "admin123"
    }