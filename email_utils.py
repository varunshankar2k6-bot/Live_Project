import smtplib
from email.mime.text import MIMEText
import logging
logger = logging.getLogger(__name__)
def send_verification_email(email, otp):
    try:
        sender_email = "varunshankar@xminds.com"
        sender_password = "qbtu dgsw etmv oslz"
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