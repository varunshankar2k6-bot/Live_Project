import smtplib
from email.mime.text import MIMEText
#Sending the emial
def send_verification_email(email, otp):
    sender_email = "varunshankar@xminds.com"
    sender_password = "qbtu etmv oslz"
    subject = "Welcome to Sports Prediction App"
    body = f"""
Welcome to Sports Prediction App ComeonDa.

Your account has been created successfully.

Your verification code is:

{otp}

Please verify your account to continue.

Thank you.
"""
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = email
    try:
        # Connect to Gmail and send mail
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(
                sender_email,
                sender_password
            )
            server.sendmail(
                sender_email,
                email,
                msg.as_string()
            )
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", e)