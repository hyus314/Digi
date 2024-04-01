let connectionCards = document.getElementsByClassName('connection-card');

// Get all connection cards

// Create and append the view message element to each card
for (const card of connectionCards) {
    const encryptedIdInput = card.querySelector('input[type="hidden"]');
    const encryptedId = encodeURIComponent(encryptedIdInput.value);

    const viewMessage = document.createElement('a');
    viewMessage.className = 'view-message';
    viewMessage.textContent = 'View';
    viewMessage.href = '/chat/?id=' + encryptedId; 

    card.appendChild(viewMessage);
}

for (const card of connectionCards) {
    const viewMessage = card.querySelector('.view-message');
    const cardBody = card.querySelector('.card-body');

    card.addEventListener('mouseenter', function () {
        cardBody.classList.add('darker');
        viewMessage.style.display = 'block';
    });

    card.addEventListener('mouseleave', function () {
        // Remove the class to reset the card body appearance
        cardBody.classList.remove('darker');
        // Hide the view message
        viewMessage.style.display = 'none';
    });
}