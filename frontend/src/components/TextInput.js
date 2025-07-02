// src/components/TextInput.js
import React, { useState } from 'react';

const TextInput = ({ onResult, onStart, addMessage }) => {
  const [input, setInput] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    setIsSubmitting(true);
    onStart();

    // Add user message to chat
    addMessage("You", input.trim(), 'text');

    try {
      const response = await fetch('http://127.0.0.1:5001/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input.trim() })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      onResult(data);
    } catch (error) {
      console.error('Error:', error);
      addMessage("System", "Sorry, I'm having trouble connecting right now. Please try again.", 'text');
    } finally {
      setIsSubmitting(false);
      setInput('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="text-input-container">
      <form onSubmit={handleSubmit} className="text-input-form">
        <div className="input-wrapper">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Share your thoughts and feelings here..."
            className="text-input"
            rows="3"
            disabled={isSubmitting}
          />
          <button 
            type="submit" 
            className="submit-button"
            disabled={isSubmitting || !input.trim()}
          >
            {isSubmitting ? (
              <div className="loading-spinner">
                <div className="spinner"></div>
                <span>Sending...</span>
              </div>
            ) : (
              <>
                <span>Send</span>
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="22" y1="2" x2="11" y2="13"></line>
                  <polygon points="22,2 15,22 11,13 2,9"></polygon>
                </svg>
              </>
            )}
          </button>
        </div>
        <div className="input-hint">
          Press Enter to send, Shift+Enter for new line
        </div>
      </form>
    </div>
  );
};

export default TextInput;
