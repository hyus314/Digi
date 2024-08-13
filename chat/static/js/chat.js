let sendButton = document.getElementById('send');
const connectionId = document.getElementById('connectionId').value;
let other_user = '';
let logged_in_user = '';
console.log(connectionId);

window.addEventListener('load', function() {
    fetch(`/chat/get-logged-in/`)
    .then(response => response.json())
    .then(data => {
        // console.log(data.logged_in);
        logged_in_user = data.logged_in;
        console.log(logged_in_user);
    }).catch(error => {
        console.error('Error:', error);
    });

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
                'user': logged_in_user
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

// new plan:

//  since we cannot access the current logged in user from the session
//  (technically we can if we use a variable here received from the server, but I won't)
//  we will just send the message and the other variable of the json dict will be
//  NOT the SENDER, but the person we send THE MESSAGE TO
//  and that is how exactly we will save it in the database
//  and when we receive the message we will check whether the user that received the message
//  is the same as the one here saved in the other_user variable 

// none of these worked
// you should just use the local variables in js for sender and sent to usernames and 
// then actually proceed to the functionality of sending the message through out the ChatConsumer
// and then you will see sender username correct in both user's screens

// Incoming message LIVE

// For all messages you will create a get request when the whole page is loaded.

const chatBox = document.querySelector('.chat-box');

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    // this is the standart code from the documentation:
    // document.querySelector('#chat-log').value += (data.message + '\n');

    const message = data.message;
    const user = data.user;
    let messageDiv = document.createElement('div');
    let messageText = document.createElement('p');
    messageText.innerHTML = message;
    messageDiv.classList.add('message-line');
    if (user == logged_in_user) {
        messageDiv.classList.add('receiver');
    } else if (user == other_user) {
        messageDiv.classList.add('sender');
    } else {
        alert('error another user');
    }
    messageDiv.appendChild(messageText);
    chatBox.appendChild(messageDiv);
    console.log(data);
}; 

// Handle error here:

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
