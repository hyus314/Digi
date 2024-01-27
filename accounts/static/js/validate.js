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

    message.innerHTML = 'Usernames should include alphanumerical lowercase characters, underscores (_) and/or hyphens(-).'
    lineDivs[1].insertAdjacentElement('beforebegin', message);
});

usernameInput.addEventListener('blur', function (event) {
    let formChildren = document.getElementsByClassName('inputs-div')[0];
    let elements = formChildren.querySelectorAll('p.lead.message');
    for (const element of elements) {
        formChildren.removeChild(element);
    }
});

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
