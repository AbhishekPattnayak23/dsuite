import { AppointmentBookingData, AppointmentCancellationData } from '../types';
const APP_BASE_URL = process.env.APP_BASE_URL || 'https://yourapp.com';

export const bookingConfirmationTemplate = (data: AppointmentBookingData) => ({
  subject: `Appointment Confirmed - ${data.serviceName} on ${data.appointmentDate}`,
  html: `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <h1 style="color: #2563eb;">Appointment Confirmed!</h1>
      <p>Hi ${data.userName},</p>
      <p>Your appointment has been successfully booked. Here are the details:</p>

      <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #374151; margin-top: 0;">Appointment Details</h3>
        <p><strong>Service:</strong> ${data.serviceName}</p>
        <p><strong>Date:</strong> ${data.appointmentDate}</p>
        <p><strong>Time:</strong> ${data.appointmentTime}</p>
        <p><strong>Appointment ID:</strong> ${data.appointmentId}</p>
        ${data.providerName ? `<p><strong>Provider:</strong> ${data.providerName}</p>` : ''}
      </div>

      <p>You can manage your appointment <a href="${APP_BASE_URL}/appointments/${data.appointmentId}" style="color: #2563eb;">here</a>.</p>

      <p>If you need to cancel or reschedule, please do so at least 24 hours in advance.</p>

      <p>Thanks,<br>The Team</p>
    </div>
  `,
  text: `Hi ${data.userName},\n\nYour appointment has been successfully booked:\n\nService: ${data.serviceName}\nDate: ${data.appointmentDate}\nTime: ${data.appointmentTime}\nAppointment ID: ${data.appointmentId}\n${data.providerName ? `Provider: ${data.providerName}\n` : ''}\nManage your appointment: ${APP_BASE_URL}/appointments/${data.appointmentId}\n\nIf you need to cancel or reschedule, please do so at least 24 hours in advance.\n\nThanks,\nThe Team`
});

export const cancellationConfirmationTemplate = (data: AppointmentCancellationData) => ({
  subject: `Appointment Cancelled - ${data.serviceName}`,
  html: `
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
      <h1 style="color: #dc2626;">Appointment Cancelled</h1>
      <p>Hi ${data.userName},</p>
      <p>Your appointment has been successfully cancelled. Here are the details:</p>

      <div style="background-color: #f3f4f6; padding: 20px; border-radius: 8px; margin: 20px 0;">
        <h3 style="color: #374151; margin-top: 0;">Cancelled Appointment</h3>
        <p><strong>Service:</strong> ${data.serviceName}</p>
        <p><strong>Date:</strong> ${data.appointmentDate}</p>
        <p><strong>Time:</strong> ${data.appointmentTime}</p>
        <p><strong>Appointment ID:</strong> ${data.appointmentId}</p>
        ${data.cancellationReason ? `<p><strong>Cancellation Reason:</strong> ${data.cancellationReason}</p>` : ''}
      </div>

      <p>If you'd like to schedule a new appointment, please visit <a href="${APP_BASE_URL}/book-appointment" style="color: #2563eb;">our booking page</a>.</p>

      <p>Thanks,<br>The Team</p>
    </div>
  `,
  text: `Hi ${data.userName},\n\nYour appointment has been successfully cancelled:\n\nService: ${data.serviceName}\nDate: ${data.appointmentDate}\nTime: ${data.appointmentTime}\nAppointment ID: ${data.appointmentId}\n${data.cancellationReason ? `Cancellation Reason: ${data.cancellationReason}\n` : ''}\n\nTo schedule a new appointment, visit: ${APP_BASE_URL}/book-appointment\n\nThanks,\nThe Team`
});
