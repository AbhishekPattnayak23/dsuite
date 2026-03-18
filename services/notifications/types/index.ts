export interface EmailNotification {
  to: string;
  subject: string;
  html: string;
  text?: string;
}

export interface AppointmentBookingData {
  userName: string;
  userEmail: string;
  appointmentDate: string;
  appointmentTime: string;
  serviceName: string;
  appointmentId: string;
  providerName?: string;
}

export interface AppointmentCancellationData {
  userName: string;
  userEmail: string;
  appointmentDate: string;
  appointmentTime: string;
  serviceName: string;
  appointmentId: string;
  cancellationReason?: string;
}

export interface NotificationResult {
  success: boolean;
  messageId?: string;
  error?: string;
}
