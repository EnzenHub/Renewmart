from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from typing import Optional
import os
from app.core.config import settings

# Email configuration
conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME", "208R1A6692@gmail.com"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD", "ziun heis btjm rcrq"),
    MAIL_FROM=os.getenv("MAIL_FROM", "208R1A6692@gmail.com"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_password_reset_otp(email: str, otp: str, user_name: str = "User"):
    """Send password reset OTP to user's email"""
    
    message = MessageSchema(
        subject="Password Reset - RenewMart",
        recipients=[email],
        body=f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>Hello {user_name},</p>
            <p>You have requested to reset your password for your RenewMart account.</p>
            <p>Your OTP (One-Time Password) is: <strong>{otp}</strong></p>
            <p>This OTP will expire in 10 minutes.</p>
            <p>If you did not request this password reset, please ignore this email.</p>
            <br>
            <p>Best regards,<br>RenewMart Team</p>
        </body>
        </html>
        """,
        subtype="html"
    )
    
    fm = FastMail(conf)
    await fm.send_message(message)
