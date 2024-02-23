window.addEventListener('load', async function () {
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


generateButton.addEventListener('click', async function() {
    let date = new Date();
    
    let days = String(date.getDate());
    console.log(days);
    let hours = String(date.getHours());
    let minutes = String(date.getMinutes());
    
    let bodyData = JSON.stringify({'hours': hours, 'minutes': minutes, 'day': days});

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
        console.log(data);
    })
    .catch(error => {
        console.error('Error:', error);
    })
});

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
    beforeSend: function(xhr, settings) {
        if (!this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});
