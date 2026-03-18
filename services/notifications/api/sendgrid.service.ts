import sgMail from '@sendgrid/mail';
import { EmailNotification, NotificationResult } from '../types';

// Configure SendGrid
const API_KEY = process.env.SENDGRID_API_KEY;
if (!API_KEY) {
  throw new Error('SENDGRID_API_KEY is not configured');
}

sgMail.setApiKey(API_KEY);

const FROM_EMAIL = process.env.SENDGRID_FROM_EMAIL || 'noreply@yourapp.com';
const FROM_NAME = process.env.SENDGRID_FROM_NAME || 'Your App Name';

export class SendGridEmailService {
  async sendEmail(notification: EmailNotification): Promise<NotificationResult> {
    try {
      const msg = {
        to: notification.to,
        from: {
          email: FROM_EMAIL,
          name: FROM_NAME
        },
        subject: notification.subject,
        html: notification.html,
        text: notification.text,
      };

      const response = await sgMail.send(msg);

      return {
        success: true,
        messageId: response[0]?.headers?.['x-message-id'] || 'unknown'
      };
    } catch (error: any) {
      console.error('SendGrid email error:', error);

      return {
        success: false,
        error: error.response?.body?.errors?.[0]?.message || error.message || 'Failed to send email'
      };
    }
  }

  async sendBatchEmails(notifications: EmailNotification[]): Promise<NotificationResult[]> {
    const results = await Promise.all(
      notifications.map(notification => this.sendEmail(notification))
    );

    return results;
  }
}
