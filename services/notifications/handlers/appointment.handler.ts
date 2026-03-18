import { SendGridEmailService } from '../api/sendgrid.service';
import {
  AppointmentBookingData,
  AppointmentCancellationData,
  NotificationResult
} from '../types';
import {
  bookingConfirmationTemplate,
  cancellationConfirmationTemplate
} from '../components/emailTemplates';

const emailService = new SendGridEmailService();

export async function sendBookingConfirmation(data: AppointmentBookingData): Promise<NotificationResult> {
  const template = bookingConfirmationTemplate(data);

  const notification = {
    to: data.userEmail,
    subject: template.subject,
    html: template.html,
    text: template.text
  };

  return await emailService.sendEmail(notification);
}

export async function sendCancellationConfirmation(data: AppointmentCancellationData): Promise<NotificationResult> {
  const template = cancellationConfirmationTemplate(data);

  const notification = {
    to: data.userEmail,
    subject: template.subject,
    html: template.html,
    text: template.text
  };

  return await emailService.sendEmail(notification);
}

// Helper function to send both notifications (useful for admin/backup notifications)
export async function sendAdminBookingNotification(
  data: AppointmentBookingData,
  adminEmail: string
): Promise<NotificationResult> {
  const template = bookingConfirmationTemplate(data);

  const notification = {
    to: adminEmail,
    subject: `[ADMIN] ${template.subject}`,
    html: template.html.replace(
      '<h1 style="color: #2563eb;">Appointment Confirmed!</h1>',
      '<h1 style="color: #2563eb;">[ADMIN] New Appointment Booked</h1>'
    ),
    text: `[ADMIN] New appointment booked:\n\n` + template.text
  };

  return await emailService.sendEmail(notification);
}
