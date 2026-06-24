from datetime import datetime, timedelta
from jose import jwt
import logging
logger = logging.getLogger(__name__)
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
def create_access_token(data: dict):
    try:
        payload = data.copy()
        payload["exp"] = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except Exception:
        logger.error("JWT creation failed", exc_info=True)
        raise