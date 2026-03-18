const nodemailer = require('nodemailer');

class EmailService {
  constructor() {
    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST,
      port: process.env.SMTP_PORT,
      secure: process.env.SMTP_PORT === '465',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS
      }
    });
  }

  async sendBookingConfirmation(email, appointmentDetails) {
    try {
      const mailOptions = {
        from: process.env.EMAIL_FROM,
        to: email,
        subject: 'Appointment Booking Confirmed',
        html: `
          <h2>Appointment Confirmed!</h2>
          <p>Dear User,</p>
          <p>Your appointment has been successfully booked.</p>
          <h3>Appointment Details:</h3>
          <ul>
            <li><strong>Location:</strong> ${appointmentDetails.location}</li>
            <li><strong>Date:</strong> ${appointmentDetails.date}</li>
            <li><strong>Time:</strong> ${appointmentDetails.startTime} - ${appointmentDetails.endTime}</li>
          </ul>
          <p>We look forward to seeing you!</p>
          <p>Best regards,<br>Appointment Booking Team</p>
        `
      };

      const info = await this.transporter.sendMail(mailOptions);
      console.log('Email sent:', info.response);
      return true;
    } catch (error) {
      console.error('Error sending email:', error);
      return false;
    }
  }
}

module.exports = EmailService;
