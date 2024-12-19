const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

let conversationHistory = [];
let isProcessing = false;

function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    
    if (!isUser) {
        // Add typing animation for bot messages
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-animation';
        messageDiv.appendChild(typingDiv);
        
        // Simulate typing effect
        let i = 0;
        const typing = setInterval(() => {
            if (i < content.length) {
                typingDiv.textContent += content[i];
                i++;
                chatMessages.scrollTop = chatMessages.scrollHeight;
            } else {
                clearInterval(typing);
            }
        }, 30);
    } else {
        messageDiv.textContent = content;
    }
    
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

async function sendMessage() {
    if (isProcessing) return;
    
    const message = userInput.value.trim();
    if (!message) return;

    isProcessing = true;
    sendButton.disabled = true;
    
    addMessage(message, true);
    userInput.value = '';

    conversationHistory.push({"role": "user", "content": message});

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                history: conversationHistory
            })
        });

        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        addMessage(data.response);
        conversationHistory.push({"role": "assistant", "content": data.response});

    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error. Please try again.');
    } finally {
        isProcessing = false;
        sendButton.disabled = false;
    }
}

// Event listeners
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Focus input on load
userInput.focus();
  
