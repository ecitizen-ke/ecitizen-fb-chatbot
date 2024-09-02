import React, { useState } from 'react';
import axios from 'axios';
import './chatbot.css';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim()) {
      // Add the user's message to the chat
      setMessages([...messages, { text: input, sender: 'user' }]);

      try {
        // Send the user's message to the API
        const response = await axios.post('http://localhost:5000/api/v1/chatbot/ai', {
          question: input
        });

        // Extract the answer from the API response
        const botMessage = response.data.answer;

        // Add the bot's response to the chat
        setMessages(prev => [...prev, { text: botMessage, sender: 'bot' }]);

      } catch (error) {
        // Handle any errors that occur during the API request
        console.error('Error fetching chatbot response:', error);
        setMessages(prev => [...prev, { text: "Sorry, something went wrong.", sender: 'bot' }]);
      }

      // Clear the input field
      setInput('');
    }
  };

  return (
    <div className="chatbot">
      <div className="chat-window">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.sender}`}>
            {message.text}
          </div>
        ))}
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
