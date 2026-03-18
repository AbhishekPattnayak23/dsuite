import React, { useState } from 'react';

const BookingForm = ({ slotId, onComplete, onCancel }) => {
  const [formData, setFormData] = useState({
    user_name: '',
    user_email: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch('/api/appointments/book', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          slot_id: slotId,
          ...formData
        })
      });

      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.detail || 'Booking failed');
      }

      onComplete(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="booking-form">
      <h2>Book Appointment</h2>

      <form onSubmit={handleSubmit}>
        {error && <div className="error">{error}</div>}

        <div className="form-group">
          <label>Name:</label>
          <input
            type="text"
            value={formData.user_name}
            onChange={(e) => setFormData({...formData, user_name: e.target.value})}
            required
          />
        </div>

        <div className="form-group">
          <label>Email:</label>
          <input
            type="email"
            value={formData.user_email}
            onChange={(e) => setFormData({...formData, user_email: e.target.value})}
            required
          />
        </div>

        <div className="button-group">
          <button type="submit" disabled={loading}>
            {loading ? 'Booking...' : 'Confirm Booking'}
          </button>
          <button type="button" onClick={onCancel} disabled={loading}>
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default BookingForm;
