const ChatManager = {
    currentChatUserId: null,
    currentChatNumber: null,
  
    scrollToBottom() {
      const chatWindow = document.getElementById('scroll-box');
      chatWindow.scrollTo({
        top: chatWindow.scrollHeight,
        behavior: 'smooth' // Smooth scrolling effect
      });
      console.log("scrolling..");
    },
  
    // Load a specific chat by user_id and chat_number
    loadChat(userId, chatNumber) {
      this.currentChatUserId = userId;
      this.currentChatNumber = chatNumber;
      const inputField = document.getElementById('input-message');
      inputField.placeholder = `You are now chatting in Chat ${chatNumber}`;
  
      fetch(`/chat/${userId}/${chatNumber}/history`)
        .then(response => response.json())
        .then(data => {
          UIManager.clearChatWindow();
          data.messages.forEach(msg =>
            UIManager.appendMessage(msg.message, msg.sender === 'user')
          );
        //   this.scrollToBottomQuick();
        UIManager.scrollToBottomQuick();
        });
    },
  
  
    
    // Send a message
    sendMessage() {
      const input = document.getElementById('input-message');
      const message = input.value;
      const spinner = document.getElementById('loading-spinner');
  
      if (!message.trim() || !this.currentChatUserId || !this.currentChatNumber) return;
  
      if (spinner) {
        spinner.style.display = 'block';
      }
  
      fetch(`/chat/${this.currentChatUserId}/${this.currentChatNumber}/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message }),
      })
        .then(response => response.json())
        .then(data => {
          UIManager.appendMessage(data.user_message, true);
          UIManager.appendMessage(data.assistant_message, false);
          this.scrollToBottom();
          input.value = '';
          if (spinner) {
            spinner.style.display = 'none';
            this.scrollToBottom();
          }
        })
        .catch(error => {
          console.error('Error sending message:', error);
          if (spinner) {
            spinner.style.display = 'none';
            
          }
        });
    },
  
    // Create a new chat
    createNewChat() {
      fetch('/chat/new', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
          this.loadChat(data.user_id, data.chat_number);
          this.updateChatList();
        });
    },
  
    updateChatList() {
      fetch('/chat-history')
        .then(response => response.json())
        .then(data => {
          UIManager.clearChatHistoryList();
  
          if (data.chats.length === 0) {
            this.createNewChat();
          } else {
            data.chats.forEach(chat =>
              UIManager.createChatHistoryItem(chat.user_id, chat.chat_number)
            );
  
            if (!this.currentChatUserId || !this.currentChatNumber) {
              const firstChat = data.chats[0];
              this.loadChat(firstChat.user_id, firstChat.chat_number);
  
            }
          }
        });
    },
  
    handleKeyPress(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        // Prevent default behavior of creating a new line
        event.preventDefault();
        this.sendMessage();
      } else if (event.key === 'Enter' && event.shiftKey) {
        // Allow default behavior (new line)
        return;
      }
    },
  
    deleteChat(userId, chatNumber) {
      console.log(`Delete button clicked for chat ${chatNumber}`);
    
      fetch(`/chat/${userId}/${chatNumber}/delete`, {
        method: 'DELETE',
        headers: {
          'Content-Type': 'application/json', // Optional, depends on your server's needs
        },
      })
        .then((response) => {
          if (response.ok) {
            console.log(`Chat ${chatNumber} for user ${userId} deleted successfully.`);
            this.updateChatList(); // Update UI
          } else {
            console.error(`Failed to delete chat ${chatNumber}. Status: ${response.status}`);
            return response.json().then((errorData) => {
              throw new Error(errorData.message || 'Unknown error occurred');
            });
          }
        })
        .catch((error) => {
          console.error(`Error occurred while deleting chat ${chatNumber}:`, error.message);
          alert(`Failed to delete chat. Please try again later.`);
        });
    },
  };