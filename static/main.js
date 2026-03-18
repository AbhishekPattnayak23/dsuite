// Slot fetching functionality
document.getElementById('cta-button')?.addEventListener('click', async () => {
    const response = await fetch('/api/slots');
    const slots = await response.json();

    const container = document.getElementById('slot-cards');
    container.innerHTML = '';

    slots.forEach(slot => {
        const card = document.createElement('div');
        card.className = 'bg-white p-4 rounded shadow';
        card.innerHTML = `
            <h4 class="font-semibold">${slot.date} ${slot.time}</h4>
            <p class="text-green-600">${slot.available ? 'Available' : 'Booked'}</p>
            <button class="mt-2 bg-blue-600 text-white px-3 py-1 rounded">Book Now</button>
        `;
        container.appendChild(card);
    });
});

// Auth form handling
document.getElementById('auth-form')?.addEventListener('submit', (e) => {
    e.preventDefault();
    sessionStorage.setItem('authenticated', 'true');
    window.location.href = '/';
});
