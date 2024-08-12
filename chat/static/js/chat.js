let sendButton = document.getElementById('send');
const connectionId = document.getElementById('connectionId').value;
let other_user = '';
console.log(connectionId);

window.addEventListener('load', function() {
    fetch(`/chat/get-connection-user/?connection_id=${encodeURIComponent(connectionId)}`)
    .then(response => response.json())
    .then(data => {
    //    console.log(data);
        const chatWithDiv = document.querySelector('body > div.title-line > p');
        chatWithDiv.innerHTML = '';
        const pElement = document.createElement('p');
        pElement.innerHTML = `chat with ${data.other_user}`;
        chatWithDiv.appendChild(pElement);
        document.title = `Chat - ${data.other_user}`;
        other_user = data.other_user;
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

//  this has to be done using the session user name, because that will be always the sender's username
//  whether the sender is this user or the other one will determine the .onmessage function

sendButton.addEventListener('click', (e) => {
    const messageInputDom = document.querySelector('#messageInput');
            const message = messageInputDom.value;
            chatSocket.send(JSON.stringify({
                'message': message,
                'user': other_user
            }));
            messageInputDom.value = '';
    e.preventDefault();
    console.log('clicked');
});

//  send the message with the username
//  receive a message using a json dictionary with keys message and user
//  if user == other_user render as the message of the other user if not render as yours
//  all you have to do is change the sender in the database
//  the model construction

// Incoming message LIVE

// For all messages you will create a get request when the whole page is loaded.

const chatBox = document.querySelector('.chat-box');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);

    // this is the standart code from the documentation:
    // document.querySelector('#chat-log').value += (data.message + '\n');

    
    console.log('here ?');
    console.log(data);
}; 

// Handle error here:

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
