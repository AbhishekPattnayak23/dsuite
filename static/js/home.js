let currentUser = null;

function init() {
    loadUserStatus();
    setDefaultDate();
    loadMyBookings();
}

function setDefaultDate() {
    const today = new Date();
    const tomorrow = new Date(today);
    tomorrow.setDate(tomorrow.getDate() + 1);
    const dateStr = tomorrow.toISOString().split('T')[0];
    document.getElementById('date-picker').value = dateStr;
}

async function loadUserStatus() {
    try {
        const response = await fetch('/api/user/status');
        const data = await response.json();

        if (data.logged_in) {
            currentUser = data;
            document.getElementById('auth-indicator').classList.remove('d-none');
            document.getElementById('auth-login').classList.add('d-none');
            document.getElementById('username').textContent = data.username;

            if (data.is_admin) {
                document.getElementById('admin-link').classList.remove('d-none');
            }
        } else {
            document.getElementById('auth-indicator').classList.add('d-none');
            document.getElementById('auth-login').classList.remove('d-none');
        }
    } catch (error) {
        console.error('Error checking user status:', error);
    }
}

async function searchSlots() {
    const location = document.getElementById('location-select').value;
    const date = document.getElementById('date-picker').value;

    if (!currentUser && !location && !date) {
        showToast('Please login and select location and date');
        return;
    }

    try {
        const params = new URLSearchParams();
        if (location) params.append('location', location);
        if (date) params.append('date', date);

        const response = await fetch(`/api/slots?${params}`);
        const slots = await response.json();

        renderSlots(slots);
    } catch (error) {
        showToast('Error loading slots');
    }
}

function renderSlots(slots) {
    const container = document.getElementById('slots-container');
    container.innerHTML = '';

    if (slots.length === 0) {
        container.innerHTML = '<div class="col-12 text-center"><p>No slots available</p></div>';
        return;
    }

    slots.forEach(slot => {
        const slotCard = document.createElement('div');
        slotCard.className = 'col-md-6 mb-3';
        slotCard.innerHTML = `
            <div class="card slot-card">
                <div class="card-body">
                    <h6 class="card-title">${slot.location}</h6>
                    <p class="card-text">
                        <small>Date: ${new Date(slot.start_time).toLocaleDateString()}</small><br>
                        <small>Time: ${new Date(slot.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</small>
                    </p>
                    ${currentUser ?
                        `<button class="btn btn-primary btn-sm" onclick="bookSlot(${slot.slot_id})">Book Slot</button>` :
                        '<small class="text-muted">Login to book</small>'
                    }
                </div>
            </div>
        `;
        container.appendChild(slotCard);
    });
}

async function bookSlot(slotId) {
    if (!currentUser) {
        showToast('Please login to book');
        return;
    }

    try {
        const response = await fetch('/api/slots/book', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${getCookie('sessionToken')}`
            },
            body: JSON.stringify({ slot_id: slotId })
        });

        if (response.ok) {
            showToast('Slot booked successfully!');
            searchSlots();
            loadMyBookings();
        } else {
            const data = await response.json();
            showToast(data.error || 'Booking failed');
        }
    } catch (error) {
        showToast('Error booking slot');
    }
}

async function loadMyBookings() {
    if (!currentUser) {
        document.getElementById('no-bookings').style.display = 'block';
        return;
    }

    try {
        const response = await fetch('/api/bookings/mine');
        const bookings = await response.json();

        const container = document.getElementById('my-bookings');
        container.innerHTML = '';

        if (bookings.length === 0) {
            document.getElementById('no-bookings').style.display = 'block';
            return;
        }

        document.getElementById('no-bookings').style.display = 'none';

        bookings.forEach(booking => {
            const li = document.createElement('li');
            li.className = 'list-group-item booking-item';
            li.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>Ref: ${booking.reference_code}</strong><br>
                        <small>${booking.location} - ${booking.date} at ${booking.time}</small>
                    </div>
                    <button class="btn btn-outline-danger btn-sm" onclick="cancelBooking(${booking.booking_id})">Cancel</button>
                </div>
            `;
            container.appendChild(li);
        });
    } catch (error) {
        console.error('Error loading bookings:', error);
    }
}

async function cancelBooking(bookingId) {
    if (!confirm('Are you sure you want to cancel this booking?')) return;

    try {
        const response = await fetch(`/api/bookings/${bookingId}/cancel`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${getCookie('sessionToken')}`
            }
        });

        if (response.ok) {
            showToast('Booking canceled');
            loadMyBookings();
            searchSlots();
        } else {
            showToast('Cancellation failed');
        }
    } catch (error) {
        showToast('Error canceling booking');
    }
}

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    const toast = document.createElement('div');
    toast.className = `toast align-items-center text-white bg-${type === 'error' ? 'danger' : 'success'} border-0`;
    toast.role = 'alert';
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${message}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    container.appendChild(toast);
    new bootstrap.Toast(toast).show();
}

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

async function logout() {
    const token = getCookie('sessionToken');
    if (!token) return;

    try {
        await fetch('/api/logout', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
    } catch (error) {
        console.error('Logout error:', error);
    }

    document.cookie = 'sessionToken=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.reload();
}

// Event listeners
document.getElementById('location-select').addEventListener('change', searchSlots);
document.getElementById('date-picker').addEventListener('change', searchSlots);

// Initialize on page load
document.addEventListener('DOMContentLoaded', init);
