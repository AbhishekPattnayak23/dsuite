from config import SENDGRID_API_KEY, MAIL_DEFAULT_SENDER
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import os

class NotificationService:
    def __init__(self):
        self.sg = SendGridAPIClient(api_key=SENDGRID_API_KEY or os.getenv('SENDGRID_API_KEY'))
        self.default_sender = MAIL_DEFAULT_SENDER or os.getenv('MAIL_DEFAULT_SENDER')

    def send_email(self, to_email, subject, html_content):
        message = Mail(
            from_email=self.default_sender,
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )

        try:
            self.sg.send(message)
            return True
        except Exception as e:
            print(f"SendGrid error: {str(e)}")
            return False

    def send_booking_confirmation(self, user_id, appointment):
        from app.models import User
        user = User.query.get(user_id)
        if not user:
            return

        slot = appointment.slot
        subject = f"Booking Confirmation - {slot.location} on {slot.date}"

        html_content = f"""
        <html>
        <body>
            <h2>Booking Confirmed!</h2>
            <p>Hi {user.username},</p>
            <p>Your appointment has been successfully booked.</p>
            <ul>
                <li><strong>Location:</strong> {slot.location}</li>
                <li><strong>Date:</strong> {slot.date}</li>
                <li><strong>Appointment ID:</strong> {appointment.id}</li>
            </ul>
        </body>
        </html>
        """

        self.send_email(user.email, subject, html_content)
