let sendButton = document.getElementById('send');
const connectionId = document.getElementById('connectionId').value;
console.log(connectionId);


const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + decodeURIComponent(connectionId)
    + '/'
);

sendButton.addEventListener('click', (e) => {
    // const messageInputDom = document.querySelector('#chat-message-input');
    //         const message = messageInputDom.value;
    //         chatSocket.send(JSON.stringify({
    //             'message': message
    //         }));
    //         messageInputDom.value = '';
    e.preventDefault();
    console.log('clicked');
});


// Incoming message LIVE

// For all messages you will create a get request when the whole page is loaded.

// chatSocket.onmessage = function(e) {
//     const data = JSON.parse(e.data);
//     document.querySelector('#chat-log').value += (data.message + '\n');
// }; 

// Handle error here:

// chatSocket.onclose = function(e) {
//     console.error('Chat socket closed unexpectedly');
// };
