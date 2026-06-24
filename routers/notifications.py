from fastapi import APIRouter
import logging
router = APIRouter(prefix="/notifications", tags=["Notifications"])
logger = logging.getLogger(__name__)
#Notifications
@router.get("/")
def get_notifications():
    try:
        return {
            "status": "success",
            "response": "Notifications fetched",
            "data": [
                "Welcome to Sports Prediction App"
            ]
        }
#Exception handling
    except Exception:
        logger.error("Notification error", exc_info=True)
        return {
            "status": "error",
            "response": "Failed to fetch notifications",
            "data": []
        }