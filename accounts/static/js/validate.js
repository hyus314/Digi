// username:

let lineDivs = document.getElementsByClassName('line-div');
let usernameInput = document.getElementById('username');
let regex = /^[a-z0-9_-]{3,16}$/;

usernameInput.addEventListener('focus', function (event) {
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
    let message = document.createElement('p');
    message.classList.add('lead');
    message.classList.add('message');
    message.style.color = 'white';
    message.style.paddingLeft = '1em';

    message.innerHTML = 'Please use only alphabetical characters.'
    lineDivs[3].insertAdjacentElement('beforebegin', message);
}

// password:

let password = document.getElementById('password');
let confirmation = document.getElementById('confirmation');
let password_regex = /^(?=.*[A-Z])(?=.*[0-9])[a-zA-Z0-9]{8,20}$/;
let password_validations = document.getElementById('password-validations');

// Passwords should consist of:
// At least 8 characters,
// 20 characters max,
// At least one capital letter,
// At least one numeric character,
// Only Alphanumeric:

password.addEventListener('focus', showPasswordValidations);
confirmation.addEventListener('focus', showPasswordValidations);

password.addEventListener('blur', hidePasswordValidations);
confirmation.addEventListener('blur', hidePasswordValidations);

function showPasswordValidations() {
    password_validations.style.display = 'block';
}

function hidePasswordValidations() {
    password_validations.style.display = 'none';
}

function validatePassword() {
    
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