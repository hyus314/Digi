let sendButton = document.getElementById('send');
const connectionId = document.getElementById('connectionId').value;
console.log(connectionId);

window.addEventListener('load', function() {
    fetch(`/chat/get-connection-users/?connection_id=${encodeURIComponent(connectionId)}`)
    .then(response => response.json())
    .then(data => {
       console.log(data)
    })
    .catch(error => {
        console.error('Error:', error);
    })
});

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + connectionId
    + '/'
);

sendButton.addEventListener('click', (e) => {
    const messageInputDom = document.querySelector('#messageInput');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message
            }));
            messageInputDom.value = '';
    e.preventDefault();
    console.log('clicked');
});


// Incoming message LIVE

// For all messages you will create a get request when the whole page is loaded.

const chatBox = document.querySelector('.chat-box');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    // this is the standart code from the documentation:
    // document.querySelector('#chat-log').value += (data.message + '\n');

    

    console.log(data);
}; 

// Handle error here:

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
