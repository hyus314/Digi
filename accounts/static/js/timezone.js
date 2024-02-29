window.addEventListener('load', async function () {
    let timezoneOffset = new Date().getTimezoneOffset();

    csrf = getCookie('csrftoken')

    fetch('/tokens/set_timezone/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf
        },
        body: JSON.stringify({ timezone_offset: timezoneOffset }),
    }).then(response => response.json())
        .then(data => {
            console.log(data.message)
        });
});

