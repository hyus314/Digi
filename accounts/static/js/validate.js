// username:

let lineDivs = document.getElementsByClassName('line-div');
let usernameInput = document.getElementById('username');
let username_regex = /^[a-z0-9_-]{3,16}$/;

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

usernameInput.addEventListener('input', function (event) {
    let currentValue = document.getElementById('username').value;
    if (currentValue) {
        if (username_regex.test(currentValue)) {
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
password.addEventListener('input', validatePassword);
password.addEventListener('blur', hidePasswordValidations);

confirmation.addEventListener('focus', showPasswordValidations);
confirmation.addEventListener('input', validatePassword);
confirmation.addEventListener('blur', hidePasswordValidations);

function showPasswordValidations() {
    password_validations.style.display = 'block';
}

function hidePasswordValidations() {
    password_validations.style.display = 'none';
}

//   <i class="fa-solid fa-circle-check"></i> <---- green check for validations


function validatePassword() {
    let passwordValue = String(document.getElementById('password').value);
    let confirmationValue = document.getElementById('confirmation').value;


    let pass_length_min = document.getElementById('pass-length-min');
    if (passwordValue.length >= 8) {
        addGreenCheck(pass_length_min);
    } else {
        removeGreenCheck(pass_length_min);
    }

    let pass_length_max = document.getElementById('pass-length-max')
    if (passwordValue.length < 20 && passwordValue) {
        addGreenCheck(pass_length_max);
    } else {
        removeGreenCheck(pass_length_max);
    }

    let pass_has_capital_letter = document.getElementById('pass-capital');
    let hasCapitalLetter = false;
    for (const letter of passwordValue) {
        if (/[A-Z]/.test(letter)) {
            hasCapitalLetter = true;
            break;
        }
    }

    if (hasCapitalLetter) {
        addGreenCheck(pass_has_capital_letter);
    } else {
        removeGreenCheck(pass_has_capital_letter);
    }

    let pass_has_numeric = document.getElementById('pass-numeric');
    let hasNumeric = false;
    for (const letter of passwordValue) {
        if (/[0-9]/.test(letter)) {
            hasNumeric = true;
            break;
        }
    }


    if (hasNumeric) {
        addGreenCheck(pass_has_numeric);
    } else {
        removeGreenCheck(pass_has_numeric);
    }

    let pass_has_alphanumeric = document.getElementById('pass-alpha-numeric');
    let passDoesNotHaveAlphaNumeric = true;

    for (const letter of passwordValue) {
        if (/[^a-zA-Z0-9]/.test(letter)) {
            passDoesNotHaveAlphaNumeric = false;
            break;
        }
    }

    if (passDoesNotHaveAlphaNumeric && passwordValue) {
        addGreenCheck(pass_has_alphanumeric);
    } else {
        removeGreenCheck(pass_has_alphanumeric);
    }

    let passMatch = document.getElementById('pass-match');
    if (passwordValue === confirmationValue && passwordValue && confirmationValue) {
        addGreenCheck(passMatch);
    } else {
        removeGreenCheck(passMatch);
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