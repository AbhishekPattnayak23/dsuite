import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict
import os
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.smtp_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("EMAIL_PORT", "587"))
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.email_from = os.getenv("EMAIL_FROM")

    def send_confirmation_email(self, to_email: str, appointment_details: Dict) -> bool:
        try:
            subject = "Appointment Confirmed - Booking Details"

            # Create message
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.email_from
            message["To"] = to_email

            # HTML content
            html_content = f"""
            <html>
            <body>
                <h2>Your Appointment is Confirmed!</h2>
                <p><strong>Hi {appointment_details.get('user_name', '')},</strong></p>
                <p>Your appointment has been successfully booked.</p>

                <h3>Booking Details:</h3>
                <ul>
                    <li><strong>Location:</strong> {appointment_details['location']}</li>
                    <li><strong>Date:</strong> {appointment_details['date']}</li>
                    <li><strong>Time:</strong> {appointment_details['time']}</li>
                    <li><strong>Booking ID:</strong> #{appointment_details['booking_id']}</li>
                </ul>

                <p>Please arrive 10 minutes before your appointment time.</p>
                <p>If you need to cancel or reschedule, please reply to this email.</p>

                <p>Thank you for choosing our services!</p>
            </body>
            </html>
            """

            text_content = f"Your appointment is confirmed at {appointment_details['location']} on {appointment_details['date']} at {appointment_details['time']}"

            part1 = MIMEText(text_content, "plain")
            part2 = MIMEText(html_content, "html")

            message.attach(part1)
            message.attach(part2)

            # Send email
            server = smtplib.SMTP(self.smtp_host, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_password)
            server.sendmail(self.email_from, to_email, message.as_string())
            server.quit()

            logger.info(f"Confirmation email sent to {to_email}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False
