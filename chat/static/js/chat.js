let sendButton = document.getElementById('send');
let other_user = '';
let logged_in_user = '';
// console.log(connectionId);

const connectionId = document.getElementById('connectionId').value;

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/chat/'
    + connectionId
    + '/'
);

//  this has to be done using the session user name, because that will be always the sender's username
//  whether the sender is this user or the other one will determine the .onmessage function

const chatBox = document.querySelector('.chat-box');

// Function to fetch logged-in user and connection user data
function fetchUserData() {
    return Promise.all([
        fetch(`/chat/get-logged-in/`)
        .then(response => response.json())
            .then(data => {
                logged_in_user = data.logged_in;
                // console.log(logged_in_user);
            }),
            fetch(`/chat/get-connection-user/?connection_id=${encodeURIComponent(connectionId)}`)
            .then(response => response.json())
            .then(data => {
                const chatWithDiv = document.querySelector('body > div.title-line > p');
                chatWithDiv.innerHTML = '';
                const pElement = document.createElement('p');
                pElement.innerHTML = `chat with ${data.other_user}`;
                chatWithDiv.appendChild(pElement);
                document.title = `chat - ${data.other_user}`;
                other_user = data.other_user;
            })
        ]);
    }
    
    // Run the fetchUserData function and then set up the chatSocket.onmessage handler
    window.addEventListener('load', function() {
        fetchUserData().then(() => {
            const chatSocket = new WebSocket(
                'ws://'
                + window.location.host
                + '/ws/chat/'
                + connectionId
                + '/'
            );
            // console.log('User data fetched, setting up onmessage handler.');
            
            chatSocket.onmessage = function(e) {
                const data = JSON.parse(e.data);
                console.log('triggered at all');
                const action = data.action;
                
                if (action === 'delete') {
                    const hiddenInputField = document.querySelector(`input[value="${data.message_id}"]`);
                    if (hiddenInputField) {
                        const messageDiv = hiddenInputField.closest('.message-line');
                        
                        if (messageDiv) {
                            messageDiv.remove();
                        }
                    }
                    return;
                }
                else if (action == 'edit') {
                    console.log('triggering edit. ');
                    const hiddenInputField = document.querySelector(`input[value="${data.message_id}"]`);
                    const newMessage = data.new_message;
                    if (hiddenInputField) {
                        console.log(data.message_id);
                        console.log('triggering edit. 222');
                        const messageDiv = hiddenInputField.closest('.message-line');
                        
                        if (messageDiv) {
                            const messageP = messageDiv.querySelector('p');
                            messageP.innerHTML = newMessage;
                        }
                    }
                    return;
                }
            
                const message = data.message;
                const user = data.user;
                const encryptedMsgId = data.message_id;
                console.log(data);
                let messageDiv = document.createElement('div');
                let messageText = document.createElement('p');
                messageText.innerHTML = message;
                messageDiv.classList.add('message-line');
                
                const hiddenIdField = document.createElement('input');
                hiddenIdField.type = 'hidden'; 
                hiddenIdField.value = encryptedMsgId;
                messageDiv.appendChild(hiddenIdField);

                if (user == logged_in_user) {
                    messageDiv.classList.add('receiver');
                    messageDiv.setAttribute('data-bs-toggle', 'modal');
                    messageDiv.setAttribute('data-bs-target', '#messageModal');

                    messageDiv.addEventListener('click', function() {
                        messageDiv.classList.add('clicked-message');
                    });

                } else if (user == other_user) {
                    messageDiv.classList.add('sender');
                } else {
                    alert('Error: another user - ' + user);
                }
                
                messageDiv.appendChild(messageText);
                chatBox.appendChild(messageDiv);

                chatBox.scrollTop = chatBox.scrollHeight;

                // console.log(data);
            };


            chatSocket.onclose = function(e) {
                console.error('Chat socket closed unexpectedly');
            };

            // Send message functionality

            sendButton.addEventListener('click', (e) => {
                const messageInputDom = document.querySelector('#messageInput');
                        const message = messageInputDom.value;
                        chatSocket.send(JSON.stringify({
                            'message': message,
                            'user': logged_in_user
                        }));
                        messageInputDom.value = '';
                e.preventDefault();
                // console.log('clicked');
            });

            // Delete functionality

            const deleteBtn = document.querySelector('button.delete');
            deleteBtn.addEventListener('click', function() {
                const clickedMessage = document.getElementsByClassName('clicked-message')[0];
                const encryptedId = clickedMessage.querySelector('input');
                const modalElement = document.getElementById('messageModal');
                const modal = bootstrap.Modal.getInstance(modalElement);
                // console.log('delete button clicked');
                // console.log(encryptedId.value);
                
                chatSocket.send(JSON.stringify({
                    'action': 'delete',
                    'user': logged_in_user,
                    'message_id': encryptedId.value
                }));
                
                modal.hide();
            });
            
            // Edit functionality

            const editBtn = document.querySelector('button.edit');
            editBtn.addEventListener('click', function() {
                const clickedMessage = document.getElementsByClassName('clicked-message')[0];
                const encryptedId = clickedMessage.querySelector('input');
                const modalElement = document.getElementById('messageModal');
                const modal = bootstrap.Modal.getInstance(modalElement);
                // console.log('delete button clicked');
                // console.log(encryptedId.value);
                const editMessageContent = document.getElementById('messageContent').value;
                // console.log(editMessageContent);    
                chatSocket.send(JSON.stringify({
                    'action': 'edit',
                    'new_message': editMessageContent,
                    'user': logged_in_user,
                    'message_id': encryptedId.value
                }));
                
                modal.hide();
                // console.log('edit button clicked');
            });

        }).catch(error => {
            console.error('Error:', error);
        });
    });
