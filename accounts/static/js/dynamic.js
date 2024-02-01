let username = document.getElementById('username')
const _username_regex = /^[a-z0-9_-]{3,16}$/;

username.addEventListener('input', async function () {
    let current = document.getElementById('username').value;
    if (current && _username_regex.test(current)) {
        fetch(`/accounts/register/?username=${encodeURIComponent(current)}`)
            .then(response => response.json())
            .then(data => {
                let message = document.getElementById('exists-message');

                message.style.display = 'block';
                if (data.exists) {
                    message.textContent = 'Username is not available.'
                    username.style.backgroundColor = '#FF7F7F';
                    removeGreenCheck(message);
                } else {
                    message.textContent = 'Username is available.'
                    addGreenCheck(message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
    } else {
        clearMessage();
    }
});

username.addEventListener('blur', clearMessage);

function clearMessage() {
    let message = document.getElementById('exists-message');
    message.style.display = 'none';
}

function addGreenCheck(element) {
    if (!element.innerHTML.includes(' <i class="fa-solid fa-circle-check"></i>')) {
        element.innerHTML += ' <i class="fa-solid fa-circle-check"></i>';
    }
    element.style.color = '#83f28f';
    element.style.setProperty('color', '#83f28f', 'important');
}

function removeGreenCheck(element) {
    element.innerHTML = element.innerHTML.replace(/ <i class="fa-solid fa-circle-check"><\/i>/g, '');
    element.style.color = '';
    element.style.setProperty('color', '', 'important');
}