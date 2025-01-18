

const UIManager = {
  // Append a message to the chat window with Markdown support
  appendMessage(content, isUser) {
    const chatWindow = document.getElementById('chat-window');
    const messageContainer = document.createElement('div');
    const messageDiv = document.createElement('div');

    messageContainer.classList.add('message-container', isUser ? 'user-message' : 'assistant-message');
    messageDiv.classList.add('message', isUser ? 'user' : 'assistant');

    // Parse Markdown content using Marked.js
    // Configure marked
    marked.setOptions({
      gfm: true,
        breaks: true,
        highlight: function (code, lang) {
          return hljs.highlightAuto(code, [lang]).value;
        },
      tables: true,
      breaks: true,
      // pedantic: true,
      sanitize: false,
      smartLists: true,
    });
    const formattedContent = marked.parse(content);

    messageDiv.innerHTML = formattedContent;

    // Create a copy icon
    const copyIcon = document.createElement('img');
    copyIcon.src = 'imgs/copy_icon.png';
    copyIcon.alt = 'Copy';
    copyIcon.classList.add('copy-icon');
    copyIcon.style.cursor = 'pointer';

    // Add functionality to copy content to clipboard
    copyIcon.onclick = () => {
      navigator.clipboard.writeText(content).then(() => {
        alert('Message copied to clipboard!');
      }).catch(err => {
        console.error('Failed to copy: ', err);
      });
    };

    // Append the copy icon to the message div
    messageDiv.appendChild(copyIcon);
    messageContainer.appendChild(messageDiv);

    chatWindow.appendChild(messageContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;
  },

  clearChatWindow() {
    document.getElementById('chat-window').innerHTML = '';
  },


  clearChatHistoryList() {
    document.getElementById('chat-history-list').innerHTML = '';
  },

  scrollToBottomQuick() {
    const chatWindow = document.getElementById('scroll-box');
    chatWindow.scrollTo({
        top: chatWindow.scrollHeight, // Scroll to the bottom
        behavior: 'auto' // Instantly scroll (default behavior)
    })},


  createChatHistoryItem(userId, chatNumber) {
    const historyList = document.getElementById('chat-history-list');
    const historyItem = document.createElement('div');
    historyItem.classList.add('history-item');
    historyItem.textContent = `Agent ${chatNumber}`;
    historyItem.setAttribute('onclick', `ChatManager.loadChat(${userId}, ${chatNumber})`);

    const deleteBtn = document.createElement('button');
    deleteBtn.classList.add('delete-btn');
    deleteBtn.innerHTML = '&times;';
    deleteBtn.setAttribute('onclick', `ChatManager.deleteChat(${userId}, ${chatNumber})`);

    historyItem.appendChild(deleteBtn);
    historyList.appendChild(historyItem);

  },
};


// Load chat list on page load
window.onload = () => ChatManager.updateChatList();