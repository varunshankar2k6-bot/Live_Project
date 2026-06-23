from fastapi import APIRouter
router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)
#Getting notifications
@router.get("/")
def get_notifications():

    return {
        "message": "Notifications router working"
    }