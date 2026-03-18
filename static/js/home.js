function showToast(message, isSuccess = true) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');

    toastMessage.textContent = message;
    toast.style.display = 'block';
    toast.style.background = isSuccess ? '#28a745' : '#dc3545';

    setTimeout(() => {
        toast.style.display = 'none';
    }, 3000);
}

function bookSlot(slotId) {
    fetch(`/api/book/${slotId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                showToast(` Booking confirmed! Reference: ${data.booking_id}`);
                setTimeout(() => location.reload(), 1500);
            } else {
                showToast(` ${data.error || 'Booking failed'}`, false);
            }
        })
        .catch(error => {
            showToast(' Network error. Please try again.', false);
        });
}

// Filter slots by location
document.getElementById('locationSelect')?.addEventListener('change', function() {
    const location = this.value;
    const cards = document.querySelectorAll('.slot-card');

    cards.forEach(card => {
        if (!location || card.dataset.location === location) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

// Filter slots by date
document.getElementById('datePicker')?.addEventListener('change', function() {
    const date = this.value;
    const cards = document.querySelectorAll('.slot-card');

    cards.forEach(card => {
        if (!date || card.dataset.date === date) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
});

// Set minimum date to today
if (document.getElementById('datePicker')) {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('datePicker').min = today;
}
