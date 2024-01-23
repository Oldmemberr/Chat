document.addEventListener('DOMContentLoaded', function() {
    const chatsContainer = document.getElementById('chats');
    const messagesContainer = document.getElementById('messages');
    const messageContentInput = document.getElementById('message-content');
    const sendMessageBtn = document.getElementById('send-message-btn');


    function displayChats(chats) {
        chatsContainer.innerHTML = '';
        chats.forEach(chat => {
            const chatItem = document.createElement('li');
            chatItem.textContent = chat.name;
            chatItem.addEventListener('click', function() {
                getChatMessages(chat.id);
            });
            chatsContainer.appendChild(chatItem);
        });
    }


    function displayMessages(messages) {
        messagesContainer.innerHTML = '';
        messages.forEach(message => {
            const messageItem = document.createElement('li');
            messageItem.textContent = `${message.sender.user.username}: ${message.content}`;
            messagesContainer.appendChild(messageItem);
        });
    }


    function getChats() {
        fetch('/api/chats/')
            .then(response => response.json())
            .then(chats => {
                displayChats(chats);
            })
            .catch(error => console.error('Error:', error));
    }


    function getChatMessages(chatId) {
        fetch(`/api/messages/?chat=${chatId}`)
            .then(response => response.json())
            .then(messages => {
                displayMessages(messages);
            })
            .catch(error => console.error('Error:', error));
    }


    getChats();


    sendMessageBtn.addEventListener('click', function() {
        const chatId = 1;  //
        const messageContent = messageContentInput.value;

        fetch(`/api/messages/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                chat: chatId,
                content: messageContent,
            }),
        })
        .then(response => response.json())
        .then(data => {
            console.log('Message sent:', data);

            getChatMessages(chatId);
        })
        .catch(error => console.error('Error:', error));
    });
});