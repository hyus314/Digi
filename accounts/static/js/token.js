window.addEventListener('load', async function () {
    const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
    const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

    const button = document.querySelector('.token-btn');
    button.innerHTML = 'loading'
    button.disabled = true;
    button.classList.add('disabled');

    fetch('/tokens/token_exists/')
        .then(response => response.json())
        .then(data => {
            // console.log(data.result)
            button.classList.remove('disabled');
            button.disabled = false;
            if (data.result === false) {
                button.innerHTML = 'generate chat token'
            } else {
                button.innerHTML = 'view chat token'
            }

        })
        .catch(error => {
            console.error('Error:', error);
        })

});

const generateButton = document.getElementsByClassName('token-btn')[0];


generateButton.addEventListener('click', async function () {
    let date = new Date();

    let days = String(date.getDate());
    let hours = String(date.getHours());
    let minutes = String(date.getMinutes());
    let seconds = String(date.getSeconds());

    let bodyData = JSON.stringify({ 'hours': hours, 'minutes': minutes, 'day': days, 'seconds': seconds });

    const csrf = getCookie('csrftoken');

    fetch('/tokens/get_token/', {
        method: 'POST',
        body: bodyData,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        }
    })
        .then(response => response.json())
        .then(data => {
            populate(data);
            let copyButton = document.querySelector('#tokenModal > div > div > div.modal-body > div > button');
            copyButton.addEventListener('click', function () {
                let tokenText = document.getElementById('token').innerHTML;
                console.log(tokenText);
            });
        })
        .catch(error => {
            let tokenText = document.getElementById('token');
            tokenText.innerHTML = 'There was an error loading your token.';
            return;
        });


});

function populate(data) {
    // console.log(data);
    let tokenText = document.getElementById('token');
    tokenText.innerHTML = data.token_value;
    let tokenRow = document.getElementsByClassName('token-row')[0];
    if (!tokenRow.querySelector('button')) {
        createCopyButton(tokenRow);

    }
}

function createCopyButton(tokenRow) {
    let button = document.createElement('button');
    button.classList.add('material-symbols-outlined');
    button.innerHTML = 'content_copy';

    button.classList.add('d-inline-block');
    button.setAttribute('type', 'button');
    button.setAttribute('data-bs-container', 'body');
    button.setAttribute('data-bs-toggle', 'popover');
    button.setAttribute('data-bs-placement', 'top');
    button.setAttribute('data-bs-trigger', 'hover');
    button.setAttribute('data-bs-content', 'Copy Token');
    button.setAttribute('data-bs-html', 'true');

    tokenRow.appendChild(button);

    let popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    let popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl, {
            content: 'Copy Token',
            placement: 'top',
            html: true
        });
    });

}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

let csrftoken = getCookie('csrftoken');

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
