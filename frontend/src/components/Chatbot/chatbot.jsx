import React, { useState } from 'react';
import axios from 'axios';
import './chatbot.css';
import { useTheme } from '../../contexts/ThemeContext'; // Import useTheme

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isThinking, setIsThinking] = useState(false);
  const { theme } = useTheme(); // Use the theme context


  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      setMessages([...messages, { text: input, sender: 'user' }]);
      setIsThinking(true);

      try {
        const response = await axios.post('http://localhost:5000/api/v1/chatbot/ai', {
          question: input
        });

        // Ensure the response is a string and remove any 'undefined'
        const botMessage = String(response.data.answer).replace(/undefined$/, '').trim();

        setIsThinking(false);
        setMessages(prev => [...prev, { text: botMessage, sender: 'bot' }]);

      } catch (error) {
        console.error('Error fetching chatbot response:', error);
        setIsThinking(false);
        setMessages(prev => [...prev, { text: "Sorry, something went wrong.", sender: 'bot' }]);
      }

      setInput('');
    }
  };

  return (
    <div className={`chatbot chatbot-${theme}`}> {/* Add theme class */}
      <div className={`chat-window chat-window-${theme}`}> {/* Add theme class */}
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender} message-${theme}`}> {/* Add theme class */}
            {message.text}
          </div>
        ))}
        {isThinking && <div className={`message bot message-${theme}`}>System is thinking...</div>}
      </div>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          className={`input-${theme}`}
        />
        <button id="chatbotButton" type="submit" className={`button-${theme}`}>Send</button> {/* Add theme class */}
      </form>
    </div>
  );
};

export default Chatbot;
