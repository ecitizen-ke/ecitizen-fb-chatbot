import React, { useState } from 'react';
import axios from 'axios';
import './chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false); // New state to show "thinking" message

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      // Add the user's message to the chat
      setMessages([...messages, { text: input, sender: 'user' }]);

      // Set the "thinking" state
      setIsThinking(true);

      try {
        // Send the user's message to the API
        const response = await axios.post('http://localhost:5000/api/v1/chatbot/ai', {
          question: input
        });

        // Extract the answer from the API response
        const botMessage = response.data.answer;

        // Clear the "thinking" state and add the bot's response with typing effect
        setIsThinking(false);
        typeMessage(botMessage);

      } catch (error) {
        console.error('Error fetching chatbot response:', error);
        setIsThinking(false);
        setMessages(prev => [...prev, { text: "Sorry, something went wrong.", sender: 'bot' }]);
      }

      // Clear the input field
      setInput('');
    }
  };

  const typeMessage = (message) => {
    let index = 0;
    const typingSpeed = 50; // Milliseconds per character

    const typingInterval = setInterval(() => {
      if (index < message.length) {
        setMessages(prev => {
          const lastMessage = prev[prev.length - 1];
          if (lastMessage && lastMessage.sender === 'bot' && lastMessage.text.length < message.length) {
            return [
              ...prev.slice(0, prev.length - 1),
              { text: lastMessage.text + message[index], sender: 'bot' }
            ];
          } else {
            return [...prev, { text: message[index], sender: 'bot' }];
          }
        });
        index++;
      } else {
        clearInterval(typingInterval);
      }
    }, typingSpeed);
  };

  return (
    <div className="chatbot">
      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
        {isThinking && <div className="message bot">System is thinking...</div>} {/* Thinking indicator */}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
        />
        <button id="chatbotButton" type="submit">Send</button>
      </form>
    </div>
  );
};

export default Chatbot;
