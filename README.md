# Documentation for DIGI

Digi is a django channels chat-based web application that was developped using the following technology:
- Daphne ASGI
- Django Channels
- Redis Server
- MSSQL

Apart from HTTP, this application also has the WebSocket protocol embedded within its' structure. WebSocket is crucial for establishing connections with a live server, sending and receiving data from that server, and at the same time sending data to other users connected as well. ASGI technology is the first to help solving the problem of structurizing everything written in the last sentence. ASGI is the successor to WSGI. 

### ASGI and WSGI

Both of these terminologies are unique for Django applications and they serve as gateways for requests and responses. Since they have one common operation to complete, the difference lies within the completion itself. Let's take a look at couple of examples and realise why WSGI is not suitable for our application.

### WSGI
- Stands for Web Server Gateway Interface. Extremely popular for HTTP Django applications. Great for single handling HTTP requests and responses and that's it. Why wouldn't that be suitable for a chatting application? Picture this scenario: You are chatting with a friend and everytime you complete something in the chat, whether you are sending, editing or deleting a message, everytime you'll have to refresh the page, in order to see what your message your friend has sent to you. WSGI is a safe option for most applications, but here we need to come up with a more user-friendly interface. That's when ASGI comes in.

### ASGI 
- Stands for Asynchronous Server Gateway Interface. ASGI, as we said earlier, is the successor to WSGI and that would mean that it does everything that WSGI can, extends some functionalities and has other unique abilities. In order to understand why ASGI is so great for this case we have to go through the WebSocket protocol very quickly. Apart from HTTP, which is request and response type of protocol, WebSocket supports an open connection between the client and the server, allowing for bi-directional data to transport between the used devices. 

### WebSocket
- Key functionalities and Differences.

How is a WebSocket connection established? Let's go through the URLS first. As we all know the `https://..` beginnings of URLS WebSockets begin with ``ws://..``. In our scenario whenever a user wants to connect to a `ws://`-based server it's client browser sends a JS WebSocket 'request' to that server, this is the piece of code that establishes that:

```javascript
const chatSocket = new WebSocket(
                'ws://'
                + window.location.host
                + '/ws/chat/'
                + connectionId
                + '/'
            );
```
Where `window.location.host` is the host of our application and `connectionId` is the encrypted id that gets decrypted in the Consumers file. We'll talk about Consumers later. Within this lies a HTTP request that is sent to that server and the response is with code 101, which means Switching Protocols and afterwards the client and server are now 'speaking' in WebSocket. That is called the Handshake. Afterwards, the exchanged data between the client and server comes in a form called `frames`, where the `payload` of the data trying to be sent to the server takes that shape. After that `payload` is sent, the server (depending on how it is configured) can either send back another frame with new data to either the client that sent the first frame, or send data to all of the users connected to that server. The data sent around all the time takes the shape of the variable

`scope`

in code and that variable servers as a Python Dict that includes the type of action sent to the server, what the server would do after receiving it and how many users would it affect, in our case only two. All of this is done in the 

`consumers.py` 

file in our `chat` folder. The payload can have a crucial role for executing different forms of operations, but in our case the payload is the content of the message, the username of the sender, and the type of action to be performed (add, edit or delete). After any of these three operations the data is sent back to the other user through the asynchronous methods: 
`chat_ message`, `chat_message_delete`, `chat_message_edit`
Here is the piece of code that executes the sending back of the newly added message to the chat room, so the other user can see live:

```python
async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_content,
                "user": sender_username,
                "message_id": encrypted_message_id, 
            }
        )
```

This piece of code is executed in the 
`receive`
functionality of the consumers.py file, which is basically triggered in the 
`chatSocket.send`
function in the `chat.js` JS file located in the `chat/static/js` directory. Here is a sum-up and a basic workflow of the explanation we gave earlier:

1. Two users connect to a chatting room through WebSocket
- 'ws://'....
Here is the result in the console of the Redis chat server (we'll talk about Redis later) after the connection: 
`WebSocket HANDSHAKING /ws/chat/Z0FBQUFBQm15MjlPNXcwQWdzUGlobHl3NE4tVHlQak81NWQwbEg2Rm9MUVJyMklYcV9LdWJvQnhXWThRZUhoWlhrVnFjZElScXJlR3Z6YW9TWGdSdm9TaWN6dFloR1R5SWc9PQ==/ [127.0.0.1:51849] `  
`WebSocket CONNECT /ws/chat/Z0FBQUFBQm15MjlPNXcwQWdzUGlobHl3NE4tVHlQak81NWQwbEg2Rm9MUVJyMklYcV9LdWJvQnhXWThRZUhoWlhrVnFjZElScXJlR3Z6YW9TWGdSdm9TaWN6dFloR1R5SWc9PQ==/ [127.0.0.1:51849]`

*the cryptic info after the the third slashes are the encrypted connection id's for each of the rooms*

2. After the handshake the server can accept the frames. The important part of the frames are the payload. This terminology comes from the low-level explanation for WebSocket:

https://en.wikipedia.org/wiki/WebSocket

But what is really important for us is the 'scope' variable where we have our properties for the type of operation and the message contents.

3. Final part is the process of disconnecting from the server. Happens automatically when the user leaves the page or closes the browser. Here is how it looks on the log of the server:

WebSocket DISCONNECT /ws/chat/Z0FBQUFBQm15MjlPNXcwQWdzUGlobHl3NE4tVHlQak81NWQwbEg2Rm9MUVJyMklYcV9LdWJvQnhXWThRZUhoWlhrVnFjZElScXJlR3Z6YW9TWGdSdm9TaWN6dFloR1R5SWc9PQ==/ [127.0.0.1:51843]   

Receiving back data to the client is a symmetrical process to the systemized process we talked about earlier.
Here we have 2 key set of methods:
The three methods in the consumers.py file 
`chat_message`, `chat_message_delete`, `chat_message_edit`
and the 
`chat.onmessage`
method in the chat/static/js directory, which is executed by the client.
```python
 def chat_message(self, event):
        message = event["message"]
        user = event["user"]  # Get the sender's username
        self.send(text_data=json.dumps({
            "message": message,
            "user": user,
            "message_id": event.get("message_id"),
         }))
```
  ^^^ this method is invoked by this async_to_sync block of code
```python   
async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": message_content,
                "user": sender_username,
                "message_id": encrypted_message_id, 
            }
        )
```
the server knows to invoke the chat_message method from the 
first property of the json dict
`"type": "chat.message"`
After the chat_message method is invoked, the `chatSocket.onmessage` is triggered, and depending on the type of the operation, the front-end will adjust accordingly.
The remaining properties are sent back as data needed to render the operation in the chatting room.
