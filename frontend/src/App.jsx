import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';

function App() {
  const [sessionId] = useState(() => Math.random().toString(36).substring(7));

  return (
    <div className="app-container">
      <div className="background-shapes">
        <div className="shape shape-1"></div>
        <div className="shape shape-2"></div>
        <div className="shape shape-3"></div>
      </div>
      
      <main className="main-content">
        <header className="header glass-panel">
          <h1>AI Healthcare Assistant</h1>
          <p className="subtitle">Powered by LLM & Machine Learning</p>
          <p className="subtitle" style={{ fontSize: '11px', opacity: 0.7, marginTop: '8px' }}>Created by devcrazy AKA Abhay Goyal</p>
        </header>

        <section className="chat-section">
          <ChatInterface sessionId={sessionId} />
        </section>
      </main>
    </div>
  );
}

export default App;
