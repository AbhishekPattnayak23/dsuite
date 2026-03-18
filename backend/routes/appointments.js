const express = require('express');
const router = express.Router();
const Appointment = require('../models/Appointment');
const emailService = require('../utils/emailService');
const { body, validationResult } = require('express-validator');

// Search available appointments by location and date
router.get('/search', [
  body('location').trim().notEmpty().withMessage('Location is required'),
  body('date').isISO8601().withMessage('Valid date is required')
], async (req, res) => {
  try {
    const { location, date } = req.query;

    // Parse and normalize the date
    const searchDate = new Date(date);
    const startOfDay = new Date(searchDate);
    startOfDay.setHours(0, 0, 0, 0);
    const endOfDay = new Date(searchDate);
    endOfDay.setHours(23, 59, 59, 999);

    // Find available appointments
    const availableAppointments = await Appointment.find({
      location: location,
      date: {
        $gte: startOfDay,
        $lte: endOfDay
      },
      isBooked: false
    }).sort({ date: 1, startTime: 1 });

    res.json({
      success: true,
      appointments: availableAppointments,
      count: availableAppointments.length
    });
  } catch (error) {
    console.error('Search error:', error);
    res.status(500).json({ success: false, error: 'Search failed' });
  }
});

// Get all locations
router.get('/locations', async (req, res) => {
  try {
    const locations = await Appointment.distinct('location');
    res.json({ success: true, locations });
  } catch (error) {
    console.error('Locations error:', error);
    res.status(500).json({ success: false, error: 'Failed to fetch locations' });
  }
});

// Book an appointment
router.post('/book/:id', [
  body('email').isEmail().normalizeEmail().withMessage('Valid email is required')
], async (req, res) => {
  try {
    const errors = validationResult(req);
    if (!errors.isEmpty()) {
      return res.status(400).json({ success: false, errors: errors.array() });
    }

    const { email } = req.body;
    const { id } = req.params;

    // Find and update appointment
    const appointment = await Appointment.findById(id);

    if (!appointment) {
      return res.status(404).json({ success: false, error: 'Appointment not found' });
    }

    if (appointment.isBooked) {
      return res.status(409).json({ success: false, error: 'Appointment already booked' });
    }

    // Update appointment
    appointment.isBooked = true;
    appointment.bookedBy = {
      email: email,
      bookedAt: new Date()
    };

    await appointment.save();

    // Send confirmation email
    const emailHandler = new emailService();
    const confirmationSent = await emailHandler.sendBookingConfirmation(email, {
      location: appointment.location,
      date: appointment.date.toLocaleDateString(),
      startTime: appointment.startTime,
      endTime: appointment.endTime
    });

    res.json({
      success: true,
      message: 'Appointment booked successfully',
      appointment,
      confirmationSent
    });
  } catch (error) {
    console.error('Booking error:', error);
    res.status(500).json({ success: false, error: 'Booking failed' });
  }
});

// Get appointments for testing
router.get('/seed', async (req, res) => {
  try {
    // Seed sample data
    const sampleData = [
      {
        location: 'Downtown Clinic',
        date: new Date(),
        startTime: '09:00',
        endTime: '09:30',
        isBooked: false
      },
      {
        location: 'Downtown Clinic',
        date: new Date(),
        startTime: '10:00',
        endTime: '10:30',
        isBooked: false
      },
      {
        location: 'Westside Medical Center',
        date: new Date(),
        startTime: '11:00',
        endTime: '11:30',
        isBooked: false
      }
    ];

    const appointments = await Appointment.insertMany(sampleData);
    res.json({ success: true, message: 'Sample data created', appointments });
  } catch (error) {
    console.error('Seeding error:', error);
    res.status(500).json({ success: false, error: 'Failed to create sample data' });
  }
});

module.exports = router;
