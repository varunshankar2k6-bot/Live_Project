from datetime import datetime, timedelta
from jose import jwt
import logging

logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
from jose import jwt
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_token(data: dict):
    try:
        payload = data.copy()
        payload["exp"] = datetime.utcnow() + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    except Exception:
        logger.error("JWT creation failed", exc_info=True)
        raise
