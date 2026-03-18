import React from 'react';
import moment from 'moment';

const SlotList = ({ slots, onBook }) => {
  return (
    <div className="slot-list">
      {slots.length === 0 ? (
        <p>No available slots found for this location and date.</p>
      ) : (
        slots.map((slot) => (
          <div key={slot.id} className="slot-card">
            <h3>{slot.location}</h3>
            <p>
              {moment(slot.start_time).format('LLLL')} -{' '}
              {moment(slot.end_time).format('LT')}
            </p>
            <p>Available: {slot.available_capacity} seats</p>
            <button
              onClick={() => onBook(slot.id)}
              disabled={slot.available_capacity === 0}
            >
              Book Now
            </button>
          </div>
        ))
      )}
    </div>
  );
};

export default SlotList;
