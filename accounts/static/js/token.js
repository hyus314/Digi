window.addEventListener('load', async function () {
    fetch('token_exists/')
        .then(response => response.json())
        .then(data => {
            // console.log(data.result)
            const button = document.querySelector('.token-btn');
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