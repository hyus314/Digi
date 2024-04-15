let sendButton = document.getElementById('send');
const connectionId = document.getElementById('connectionId').value;
console.log(connectionId);
sendButton.addEventListener('click', (e) => {
    e.preventDefault();
    console.log('clicked');
});

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + decodeURIComponent(connectionId)
    + '/'
);