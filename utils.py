from passlib.context import CryptContext
import logging
logger = logging.getLogger(__name__)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def hash_password(password: str):
    try:
        return pwd_context.hash(password)
    except Exception:
        logger.error("Hash error", exc_info=True)
        raise
def verify_password(plain, hashed):
    try:
        return pwd_context.verify(plain, hashed)
    except Exception:
        logger.error("Verify error", exc_info=True)
        return False