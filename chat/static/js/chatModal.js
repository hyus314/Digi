const messageModal = document.getElementById('messageModal');

messageModal.addEventListener('shown.bs.modal', function() {
    const clickedMessage = document.getElementsByClassName('clicked-message')[0];
    const clickedMessageText = clickedMessage.querySelector('p').innerHTML;
    // console.log(clickedMessageText);
    const messageContent = document.getElementById('messageContent');
    messageContent.value = clickedMessageText;
});

messageModal.addEventListener('hidden.bs.modal', function() {
    const messageContent = document.getElementById('messageContent');
    messageContent.value = '';
    const clickedMessage = document.getElementsByClassName('clicked-message')[0];
    clickedMessage.classList.remove('clicked-message');
});