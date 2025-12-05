document.addEventListener('DOMContentLoaded', function () {
  const chatBox = document.getElementById('chat-box');
  const chatForm = document.getElementById('chat-form');
  const userInput = document.getElementById('user-input');

  // Typewriter effect
  function typeMessage(text, container, speed = 30, callback = null) {
    container.textContent = '';
    let i = 0;
    function typeChar() {
      if (i < text.length) {
        container.textContent += text.charAt(i);
        i++;
        chatBox.scrollTop = chatBox.scrollHeight;
        setTimeout(typeChar, speed);
      } else if (callback) {
        callback();
      }
    }
    typeChar();
  }

  // Append message bubble
  function appendMessage(text, sender) {
    const wrapper = document.createElement('div');
    wrapper.className = `message ${sender}`;

    const avatar = document.createElement('img');
    avatar.className = 'avatar';
    avatar.src = sender === 'user' ? '/static/user_avatar.jpg' : '/static/gaia_avatar.jpg';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';

    if (sender === 'user') {
      bubble.textContent = text;
      wrapper.appendChild(bubble);
      wrapper.appendChild(avatar);
    } else {
      wrapper.appendChild(avatar);
      wrapper.appendChild(bubble);
      typeMessage(text, bubble, 30);
    }

    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Show typing indicator
  function showTypingIndicator(callback) {
    const wrapper = document.createElement('div');
    wrapper.className = 'message ai';
    const avatar = document.createElement('img');
    avatar.className = 'avatar';
    avatar.src = '/static/gaia_avatar.jpg';
    const bubble = document.createElement('div');
    bubble.className = 'bubble typing';
    bubble.textContent = '...';
    wrapper.appendChild(avatar);
    wrapper.appendChild(bubble);
    chatBox.appendChild(wrapper);
    chatBox.scrollTop = chatBox.scrollHeight;

    setTimeout(() => {
      wrapper.remove();
      callback();
    }, 600);
  }

  // Handle form submission
  chatForm.addEventListener('submit', async function (e) {
    e.preventDefault();
    const message = userInput.value.trim();
    if (!message) return;

    appendMessage(message, 'user');
    userInput.value = '';

    showTypingIndicator(async () => {
      try {
        const response = await fetch('/message', { // Flask route
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        const data = await response.json();
        appendMessage(data.reply, 'ai');
      } catch (err) {
        appendMessage("Oops, something went wrong.", 'ai');
        console.error(err);
      }
    });
  });
});
