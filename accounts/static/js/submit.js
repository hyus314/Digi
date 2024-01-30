let submitBtn = document.getElementById('submit');

function createAlert(message) {
    // Create the main container div
    var alertDiv = document.createElement('div');
    alertDiv.classList.add('alert', 'alert-primary', 'd-flex', 'align-items-center', 'animate__animated', 'animate__fadeInDown');
    alertDiv.setAttribute('role', 'alert');

    // Create the SVG element
    var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
    svg.setAttribute('class', 'bi bi-exclamation-triangle-fill flex-shrink-0 me-2');
    svg.setAttribute('viewBox', '0 0 16 16');
    svg.setAttribute('role', 'img');
    svg.setAttribute('aria-label', 'Warning:');

    // Create the path element inside the SVG
    var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('d', 'M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z');

    // Append the path to the SVG
    svg.appendChild(path);

    // Create the div for the text
    var textDiv = document.createElement('div');
    textDiv.textContent = message;

    // Append the SVG and text divs to the main container div
    alertDiv.appendChild(svg);
    alertDiv.appendChild(textDiv);

    // Append the main container div to the document body or any other desired parent element
    return alertDiv;

}

submitBtn.addEventListener('click', function (event) {
    // username
    // /^[a-z0-9_-]{3,16}$/;

    let alertsContainer = document.getElementById('alert-container');

    // Add alerts with a delay between them
    for (let i = 0; i < 3; i++) {
        setTimeout(function () {
            let alert = createAlert('is this working?');
            alertsContainer.appendChild(alert);
    
            // Apply fade-out animation after a delay
            setTimeout(function () {
                alert.classList.add('animate__fadeOutDown');
            }, 4000); 
    
            // Remove the element from the DOM after the animation duration + delay
            setTimeout(function () {
                alert.remove();
            }, 5000); 
        }, i * 1000); // Increase the delay for each subsequent alert
    }
    

    event.preventDefault();
});
