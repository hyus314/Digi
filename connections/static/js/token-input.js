let input = document.querySelector('#input');

input.addEventListener('input', async function() {
    const value = input.value
    // console.log(value);
    let result = document.querySelector('.token-result>p');
    result.innerHTML = value; 
});