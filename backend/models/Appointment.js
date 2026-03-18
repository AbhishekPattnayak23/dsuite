const mongoose = require('mongoose');

const appointmentSchema = new mongoose.Schema({
  location: {
    type: String,
    required: true,
    trim: true
  },
  date: {
    type: Date,
    required: true
  },
  startTime: {
    type: String,
    required: true
  },
  endTime: {
    type: String,
    required: true
  },
  isBooked: {
    type: Boolean,
    default: false
  },
  bookedBy: {
    email: {
      type: String,
      trim: true,
      lowercase: true
    },
    bookedAt: {
      type: Date
    }
  }
}, {
  timestamps: true
});

// Add compound index for efficient querying
appointmentSchema.index({ location: 1, date: 1, isBooked: 1 });

const Appointment = mongoose.model('Appointment', appointmentSchema);

module.exports = Appointment;
