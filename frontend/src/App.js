import React, { useState, useEffect, useRef } from 'react';
import TextInput from './components/TextInput';
import SpeechInput from './components/SpeechInput';
import RecordAudio from './components/RecordAudio';
import './App.css';
import therapistImage from './assets/therapist.png';

function App() {
  const [chatLog, setChatLog] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [activeInput, setActiveInput] = useState('text'); // 'text', 'speech', 'audio'
  const chatEndRef = useRef(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [chatLog]);

  const addMessage = (sender, text, type = 'text', metadata = {}) => {
    const newMessage = {
      id: Date.now(),
      sender,
      text,
      type,
      timestamp: new Date().toLocaleTimeString(),
      ...metadata
    };
    setChatLog(prev => [...prev, newMessage]);
  };

  const handleTextResponse = (data) => {
    setIsLoading(false);
    addMessage("Therapist", data.response, 'text', {
      sentiment: data.overall_sentiment,
      vader: data.vader_result,
      roberta: data.roberta_result
    });
  };

  const handleVoiceResponse = (data) => {
    setIsLoading(false);
    addMessage("Therapist", data.response, 'text', {
      sentiment: data.overall_sentiment,
      vader: data.vader_result,
      roberta: data.roberta_result
    });
  };

  const handleAudioResponse = (data) => {
    setIsLoading(false);
    addMessage("Therapist", data.response, 'text', {
      sentiment: data.overall_sentiment,
      vader: data.vader_result,
      roberta: data.roberta_result
    });
  };

  const handleInputStart = () => {
    setIsLoading(true);
  };

  return (
    <div className="app-container">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="logo-section">
            <img src={therapistImage} alt="AI Therapist" className="logo-image" />
            <div className="logo-text">
              <h1>AI Speech Therapy</h1>
              <p className="subtitle">Your compassionate AI companion for emotional support</p>
            </div>
          </div>
          <div className="status-indicator">
            <div className="status-dot"></div>
            <span>Online</span>
          </div>
        </div>
      </header>

      {/* Chat Interface */}
      <div className="chat-container">
        <div className="chat-messages">
          {chatLog.length === 0 ? (
            <div className="welcome-message">
              <div className="welcome-icon">💬</div>
              <h2>Welcome to AI Speech Therapy</h2>
              <p>I'm here to listen and support you. You can:</p>
              <ul>
                <li>Type your thoughts and feelings</li>
                <li>Use voice-to-text for hands-free communication</li>
                <li>Record audio for more natural expression</li>
              </ul>
              <p className="welcome-note">Everything you share is processed locally and kept private.</p>
            </div>
          ) : (
            chatLog.map((message) => (
              <div key={message.id} className={`message ${message.sender === 'Therapist' ? 'therapist' : 'user'}`}>
                <div className="message-content">
                  <div className="message-header">
                    <span className="sender-name">{message.sender}</span>
                    <span className="timestamp">{message.timestamp}</span>
                  </div>
                  <div className="message-text">{message.text}</div>
                  {message.type === 'audio' && (
                    <div className="audio-indicator">
                      <span>🎤 Audio Message</span>
                    </div>
                  )}
                  {message.type === 'speech' && (
                    <div className="speech-indicator">
                      <span>🎙️ Voice-to-Text</span>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="message therapist">
              <div className="message-content">
                <div className="typing-indicator">
                  <div className="typing-dots">
                    <div className="dot"></div>
                    <div className="dot"></div>
                    <div className="dot"></div>
                  </div>
                  <span>AI Therapist is thinking...</span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={chatEndRef} />
        </div>

        {/* Input Section */}
        <div className="input-section">
          <div className="input-tabs">
            <button 
              className={`tab ${activeInput === 'text' ? 'active' : ''}`}
              onClick={() => setActiveInput('text')}
            >
              ✏️ Type
            </button>
            <button 
              className={`tab ${activeInput === 'speech' ? 'active' : ''}`}
              onClick={() => setActiveInput('speech')}
            >
              🎙️ Voice
            </button>
            <button 
              className={`tab ${activeInput === 'audio' ? 'active' : ''}`}
              onClick={() => setActiveInput('audio')}
            >
              🎤 Record
            </button>
          </div>

          <div className="input-content">
            {activeInput === 'text' && (
              <TextInput 
                onResult={handleTextResponse}
                onStart={handleInputStart}
                addMessage={addMessage}
              />
            )}
            {activeInput === 'speech' && (
              <SpeechInput 
                onResult={handleVoiceResponse}
                onStart={handleInputStart}
                addMessage={addMessage}
              />
            )}
            {activeInput === 'audio' && (
              <RecordAudio 
                onResult={handleAudioResponse}
                onStart={handleInputStart}
                addMessage={addMessage}
              />
            )}
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="footer">
        <p>Powered by AI • Your privacy is protected • Responses generated locally</p>
      </footer>
    </div>
  );
}

export default App;
