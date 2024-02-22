window.addEventListener('load', async function () {
    const button = document.querySelector('.token-btn');
    button.innerHTML = 'loading'
    button.disabled = true;
    button.classList.add('disabled');

    fetch('token_exists/')
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

