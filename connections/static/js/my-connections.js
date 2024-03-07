let connectionCards = document.getElementsByClassName('connection-card');

// Get all connection cards

// Create and append the view message element to each card
for (const card of connectionCards) {
    const viewMessage = document.createElement('button');
    viewMessage.className = 'view-message';
    viewMessage.textContent = 'View';
    card.appendChild(viewMessage);
}

// Add event listeners for mouseenter and mouseleave to each card
for (const card of connectionCards) {
    const viewMessage = card.querySelector('.view-message');
    const cardBody = card.querySelector('.card-body');

    card.addEventListener('mouseenter', function () {
        // Add a class to darken the card body
        cardBody.classList.add('darker');
        // Show the view message
        viewMessage.style.display = 'block';
    });

    card.addEventListener('mouseleave', function () {
        // Remove the class to reset the card body appearance
        cardBody.classList.remove('darker');
        // Hide the view message
        viewMessage.style.display = 'none';
    });
}