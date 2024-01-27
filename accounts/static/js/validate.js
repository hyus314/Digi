// username:

let lineDivs = document.getElementsByClassName('line-div');
let usernameInput = document.getElementById('username');
let regex = /^[a-z0-9_-]{3,16}$/;

usernameInput.addEventListener('focus', function (event) {
    console.log('focused');
    let message = document.createElement('p');
    message.classList.add('lead');
    message.classList.add('message');
    message.style.color = 'white';
    message.style.paddingLeft = '1em';

    message.innerHTML = 'Usernames should include alphanumerical lowercase characters, underscores (_) and/or hyphens (-).'
    lineDivs[1].insertAdjacentElement('beforebegin', message);
});

usernameInput.addEventListener('blur', clearForm);

usernameInput.addEventListener('change', function (event) {
    let currentValue = document.getElementById('username').value;
    if (currentValue) {
        if (regex.test(currentValue)) {
            usernameInput.style.backgroundColor = '#83f28f';
        } else {
            usernameInput.style.backgroundColor = '#FF7F7F';
        }
    } else {
        usernameInput.style.backgroundColor = '';
    }
});

// names:

let firstN_input = document.getElementById('first');
let lastN_input = document.getElementById('last');

firstN_input.addEventListener('focus', displayNameMessage);
lastN_input.addEventListener('focus', displayNameMessage);

firstN_input.addEventListener('blur', clearForm);
lastN_input.addEventListener('blur', clearForm);

function displayNameMessage() {
    console.log('focused');
    let message = document.createElement('p');
    message.classList.add('lead');
    message.classList.add('message');
    message.style.color = 'white';
    message.style.paddingLeft = '1em';
    
    message.innerHTML = 'Please use only alphabetical characters.'
    lineDivs[3].insertAdjacentElement('beforebegin', message);
}

// global functions:

function clearForm() {
    let divs = document.getElementsByClassName('inputs-div');
    for (const div of divs) {
        let elements = div.querySelectorAll('p.lead.message');
        for (const element of elements) {
            div.removeChild(element);
        }
    }
}