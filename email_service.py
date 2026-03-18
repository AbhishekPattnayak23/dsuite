from __future__ import annotations
import logging
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail
except ImportError:
    SendGridAPIClient = None

def send_email(to_email, subject, html_content):
    """Send email via SendGrid."""
    try:
        if not SendGridAPIClient:
            logging.info(f"Email: {subject} to {to_email}")
            return

        sg = SendGridAPIClient('SENDGRID_API_KEY')
        mail = Mail(
            from_email='noreply@domain.tld',
            to_emails=to_email,
            subject=subject,
            html_content=html_content
        )
        response = sg.send(mail)
        return response
    except Exception as e:
        logging.error(f"Email error: {e}")
