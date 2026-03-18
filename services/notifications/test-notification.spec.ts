import { SendGridEmailService } from '../api/sendgrid.service';
import { bookingConfirmationTemplate } from '../components/emailTemplates';
import { AppointmentBookingData } from '../types';

// Mock SendGrid
jest.mock('@sendgrid/mail', () => ({
  setApiKey: jest.fn(),
  send: jest.fn().mockResolvedValue([{ headers: { 'x-message-id': 'test-id' } }])
}));

describe('SendGridEmailService', () => {
  let emailService: SendGridEmailService;

  beforeEach(() => {
    emailService = new SendGridEmailService();
    process.env.SENDGRID_API_KEY = 'test-key';
    process.env.SENDGRID_FROM_EMAIL = 'test@example.com';
    process.env.SENDGRID_FROM_NAME = 'Test App';
    process.env.APP_BASE_URL = 'https://test.com';
  });

  it('should create booking confirmation template', () => {
    const data: AppointmentBookingData = {
      userName: 'Test User',
      userEmail: 'test@example.com',
      appointmentDate: '2024-01-15',
      appointmentTime: '2:00 PM',
      serviceName: 'Test Service',
      appointmentId: 'apt-123'
    };

    const template = bookingConfirmationTemplate(data);

    expect(template.subject).toContain('Appointment Confirmed');
    expect(template.html).toContain('Test User');
    expect(template.html).toContain('Test Service');
  });
});
