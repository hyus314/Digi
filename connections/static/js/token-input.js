let input = document.querySelector('#input');
const pattern = /^DG[A-Za-z0-9]{6}X$/;

input.addEventListener('input', async function () {
    const value = input.value
    slice(value);
    let tokenDiv = document.querySelector('.token-result');
    if (pattern.test(value)) {
        tokenDiv.style.backgroundColor = 'green';
    } else {
        tokenDiv.style.backgroundColor = 'black';
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