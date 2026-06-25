import smtplib
from email.mime.text import MIMEText
import logging

logger = logging.getLogger(__name__)


def send_verification_email(email, otp):
    try:
        from config import MAIL_USERNAME, MAIL_PASSWORD, MAIL_SERVER, MAIL_PORT

        sender_email = MAIL_USERNAME
        sender_password = MAIL_PASSWORD
        subject = "Sports Prediction App Verification"
        body = f"Your OTP is {otp}"
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = sender_email
        msg["To"] = email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, email, msg.as_string())
        logger.info(f"Email sent to {email}")
    except Exception:
        logger.error("Email sending failed", exc_info=True)
