// Global variables
let currentLocation = '';
let currentDate = '';
let bookings = [];

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Load bookings from hidden div
    const bookingsDiv = document.getElementById('booking-references');
    if (bookingsDiv) {
        bookings = JSON.parse(bookingsDiv.dataset.bookings || '[]');
    }

    // Set up event listeners
    document.getElementById('location-select').addEventListener('change', handleLocationChange);
    document.getElementById('date-picker').addEventListener('change', handleDateChange);
    document.getElementById('slot-cta').addEventListener('click', bookSlot);

    // Preload slots if values exist
    const locationSelect = document.getElementById('location-select');
    const datePicker = document.getElementById('date-picker');

    if (locationSelect.value && datePicker.value) {
        loadSlots();
    }
});

function handleLocationChange() {
    currentLocation = this.value;
    if (currentDate) {
        loadSlots();
    }
}

function handleDateChange() {
    currentDate = this.value;
    if (currentLocation) {
        loadSlots();
    }
}

async function loadSlots() {
    if (!currentLocation || !currentDate) {
        return;
    }

    try {
        const response = await fetch(`/api/slots?location=${encodeURIComponent(currentLocation)}&date=${encodeURIComponent(currentDate)}`);

        if (!response.ok) {
            throw new Error('Failed to load slots');
        }

        const slots = await response.json();
        renderSlots(slots);
    } catch (error) {
        showToast('Error loading slots');
        console.error('Error:', error);
    }
}

function renderSlots(slots) {
    const container = document.getElementById('slot-cards');
    container.innerHTML = '';

    if (slots.length === 0) {
        container.innerHTML = '<div class="col-12"><p class="text-center">No slots available for selected date</p></div>';
        return;
    }

    slots.forEach(slot => {
        const card = createSlotCard(slot);
        container.appendChild(card);
    });
}

function createSlotCard(slot) {
    const col = document.createElement('div');
    col.className = 'col-md-4 mb-3';

    const isAlreadyBookedByUser = bookings.some(b => b.slot_id === slot.slot_id);

    col.innerHTML = `
        <div class="card h-100">
            <div class="card-body d-flex flex-column">
                <h6 class="card-subtitle mb-2 text-muted">${new Date(slot.start_time).toLocaleDateString()}</h6>
                <h5 class="card-title">${new Date(slot.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} - ${new Date(slot.end_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</h5>
                <p class="card-text">
                    <small class="text-muted">${slot.location}</small>
                </p>
                <div class="mt-auto">
                    ${isAlreadyBookedByUser
                        ? '<span class="badge bg-success">Booked by you</span>'
                        : slot.is_booked
                        ? '<span class="badge bg-danger">Booked</span>'
                        : '<button class="btn btn-primary btn-sm slot-book-btn" data-slot-id="' + slot.slot_id + '">Book this slot</button>'
                    }
                </div>
            </div>
        </div>
    `;

    const bookBtn = col.querySelector('.slot-book-btn');
    if (bookBtn) {
        bookBtn.addEventListener('click', () => bookSlot(slot.slot_id));
    }

    return col;
}

async function bookSlot(slotId) {
    if (!slotId) return;

    try {
        const response = await fetch('/api/slots/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ slot_id: parseInt(slotId) })
        });

        if (response.ok) {
            showToast('Slot booked successfully!');
            loadSlots(); // Reload slots
            location.reload(); // Reload page to update bookings
        } else {
            const result = await response.json();
            showToast(result.error || 'Failed to book slot');
        }
    } catch (error) {
        showToast('Error booking slot');
        console.error('Error:', error);
    }
}

function showToast(message) {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = 'alert alert-info';
    toast.textContent = message;

    container.appendChild(toast);

    setTimeout(() => {
        toast.remove();
    }, 3000);
}

function logout() {
    fetch('/api/logout', { method: 'POST' })
        .then(() => {
            window.location.href = '/login';
        })
        .catch(() => {
            window.location.href = '/login';
        });
}

async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) {
        return;
    }

    try {
        const response = await fetch(`/api/bookings/${bookingId}/cancel`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            showToast('Booking cancelled successfully!');
            location.reload();
        } else {
            showToast('Failed to cancel booking');
        }
    } catch (error) {
        showToast('Error cancelling booking');
    }
}
