import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")
MAIL_SERVER = os.getenv("MAIL_SERVER")
MAIL_PORT = int(os.getenv("MAIL_PORT", 587))
