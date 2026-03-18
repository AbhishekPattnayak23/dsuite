import dotenv from 'dotenv';
import { sendBookingConfirmation, sendCancellationConfirmation } from './index';
import { AppointmentBookingData, AppointmentCancellationData } from './types';

// Load environment variables
dotenv.config();

async function testNotifications() {
  const bookingData: AppointmentBookingData = {
    userName: 'John Doe',
    userEmail: 'john.doe@example.com',
    appointmentDate: '2024-01-15',
    appointmentTime: '2:00 PM',
    serviceName: 'Consultation',
    appointmentId: 'apt-12345',
    providerName: 'Dr. Smith'
  };

  const cancellationData: AppointmentCancellationData = {
    userName: 'Jane Smith',
    userEmail: 'jane.smith@example.com',
    appointmentDate: '2024-01-15',
    appointmentTime: '3:00 PM',
    serviceName: 'Follow-up',
    appointmentId: 'apt-67890',
    cancellationReason: 'Change in schedule'
  };

  try {
    console.log('Testing booking notification...');
    const bookingResult = await sendBookingConfirmation(bookingData);
    console.log('Booking notification result:', bookingResult);

    console.log('Testing cancellation notification...');
    const cancellationResult = await sendCancellationConfirmation(cancellationData);
    console.log('Cancellation notification result:', cancellationResult);
  } catch (error) {
    console.error('Test failed:', error);
  }
}

// Only run if this file is executed directly
if (require.main === module) {
  testNotifications();
}
