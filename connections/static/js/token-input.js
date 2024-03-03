let input = document.querySelector('#input');
const pattern = /^DG[A-Za-z0-9]{6}X$/;

input.addEventListener('input', async function () {
    const value = input.value
    let csrftoken = getCookie('csrftoken');
    slice(value);
    let tokenDiv = document.querySelector('.token-result');
    let button = document.querySelector('.button-div>button');
    button.disabled = true;
    if (pattern.test(value)) {
        fetch('/tokens/check_token/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({ token: value }),
        }).then(response => response.json())
            .then(data => {
                console.log(data.message)
                if (data.message === 'yes') {
                    tokenDiv.style.backgroundColor = '#1B5E20';
                    if (button.classList.contains('disabled')){
                        button.classList.remove('disabled');
                        button.disabled = false;
                    }
                } else if (data.message === 'no') {
                    tokenDiv.style.backgroundColor = '#B71C1C';
                    if (!button.classList.contains('disabled')){
                        button.classList.add('disabled');
                        button.disabled = true;
                    }
                }
            });
    } else {
        tokenDiv.style.backgroundColor = 'black';
        if (!button.classList.contains('disabled')){
            button.classList.add('disabled');
            button.disabled = true;
        }
    }
    // console.log(value);
    let result = document.querySelector('.token-result>p');
    result.innerHTML = value;
});

function slice(value) {
    if (value.length > 9) {
        value = value.slice(0, 9);
        input.value = value;
    }
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

