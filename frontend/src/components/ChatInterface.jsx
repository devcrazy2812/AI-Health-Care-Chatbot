import React, { useState, useEffect, useRef } from 'react';
import SymptomCard from './SymptomCard';
import { Send, Activity } from 'lucide-react';

const ChatInterface = ({ sessionId }) => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello. I am your AI Healthcare Assistant. How can I help you today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:8000/api/chat/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ session_id: sessionId, message: userMessage })
      });

      const data = await response.json();
      
      setMessages(prev => [
        ...prev, 
        { 
          role: 'assistant', 
          content: data.response,
          requiresSymptoms: data.requires_symptoms 
        }
      ]);
    } catch (error) {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error: Could not connect to the healthcare server.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-container glass-panel">
      <div className="messages-area">
        {messages.map((msg, idx) => (
          <div key={idx} className={`message-wrapper message-${msg.role}`}>
            <div className={`message-bubble`}>
              {msg.role === 'assistant' && (
                <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px', opacity: 0.8, fontSize: '12px'}}>
                  <Activity size={14} /> AI Assistant
                </div>
              )}
              {msg.content}
              {msg.requiresSymptoms && (
                <div className="symptom-card-wrapper">
                  <SymptomCard />
                </div>
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message-wrapper message-bot">
            <div className="message-bubble typing-indicator">
              <span className="dot"></span>
              <span className="dot"></span>
              <span className="dot"></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form className="input-area" onSubmit={handleSend}>
        <input
          type="text"
          className="chat-input"
          placeholder="Describe your symptoms or ask a medical question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={isLoading}
        />
        <button type="submit" className="send-button" disabled={isLoading || !input.trim()}>
          <Send size={20} />
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
