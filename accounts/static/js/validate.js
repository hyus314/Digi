let lineDivs = document.getElementsByClassName('line-div');
let usernameInput = document.getElementById('username');

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
    let element = formChildren.querySelector('p.lead.message');
    formChildren.removeChild(element);
});

