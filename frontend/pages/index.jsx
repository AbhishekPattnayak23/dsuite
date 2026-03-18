import React, { useState } from 'react';
import SearchForm from '../components/SearchForm';
import SlotList from '../components/SlotList';
import BookingForm from '../components/BookingForm';
import './App.css';

function App() {
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [bookingComplete, setBookingComplete] = useState(null);

  const handleSearch = async (location, date) => {
    try {
      const response = await fetch('/api/slots/search', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ location, date })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error('Search failed');
      }

      setSlots(data);
      setSelectedSlot(null);
      setBookingComplete(null);
    } catch (error) {
      console.error('Search failed:', error);
      alert('Failed to search slots. Please try again.');
    }
  };

  const handleBook = (slotId) => {
    setSelectedSlot(slotId);
  };

  const handleBookingComplete = (result) => {
    setBookingComplete(result);
    setSelectedSlot(null);
    alert(`Booking confirmed! Check your email for details. Your booking ID is #${result.booking_id}`);
  };

  const handleBookingCancel = () => {
    setSelectedSlot(null);
  };

  return (
    <div className="app">
      <header>
        <h1>Appointment Booking System</h1>
      </header>

      <main>
        <SearchForm onSearch={handleSearch} />

        <SlotList slots={slots} onBook={handleBook} />

        {selectedSlot && (
          <BookingForm
            slotId={selectedSlot}
            onComplete={handleBookingComplete}
            onCancel={handleBookingCancel}
          />
        )}

        {bookingComplete && (
          <div className="booking-success">
            <h3>Booking Confirmed!</h3>
            <p>Your booking ID: #{bookingComplete.booking_id}</p>
            <p>Check your email for confirmation details.</p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
