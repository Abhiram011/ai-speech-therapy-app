// src/components/SpeechInput.js
import React, { useState, useEffect, useCallback } from 'react';

const SpeechInput = ({ onResult, onStart, addMessage }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const [recognition, setRecognition] = useState(null);

  const handleSubmit = useCallback(async () => {
    if (!transcript.trim()) return;

    setIsProcessing(true);
    onStart();

    // Add user message to chat
    addMessage("You", transcript.trim(), 'speech');

    try {
      const response = await fetch('http://127.0.0.1:5001/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: transcript.trim() })
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      onResult(data);
    } catch (error) {
      console.error('Error:', error);
      addMessage("System", "Sorry, I'm having trouble processing your voice input. Please try again.", 'text');
    } finally {
      setIsProcessing(false);
      setTranscript('');
    }
  }, [transcript, onStart, addMessage, onResult]);

  useEffect(() => {
    // Initialize speech recognition
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      const recognitionInstance = new SpeechRecognition();
      
      recognitionInstance.continuous = false;
      recognitionInstance.interimResults = true;
      recognitionInstance.lang = 'en-US';

      recognitionInstance.onstart = () => {
        setIsListening(true);
        setTranscript('');
      };

      recognitionInstance.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';

        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }

        setTranscript(finalTranscript + interimTranscript);
      };

      recognitionInstance.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        if (event.error === 'not-allowed') {
          addMessage("System", "Please allow microphone access to use voice input.", 'text');
        }
      };

      recognitionInstance.onend = () => {
        setIsListening(false);
        if (transcript.trim()) {
          handleSubmit();
        }
      };

      setRecognition(recognitionInstance);
    } else {
      addMessage("System", "Speech recognition is not supported in your browser. Please use text or audio recording instead.", 'text');
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [addMessage, handleSubmit]);

  const startListening = () => {
    if (recognition) {
      recognition.start();
    }
  };

  const stopListening = () => {
    if (recognition) {
      recognition.stop();
    }
  };

  const handleManualSubmit = (e) => {
    e.preventDefault();
    if (transcript.trim()) {
      handleSubmit();
    }
  };

  return (
    <div className="speech-input-container">
      <div className="speech-status">
        {isListening ? (
          <div className="listening-indicator">
            <div className="pulse-ring"></div>
            <span>Listening...</span>
          </div>
        ) : (
          <span>Click the microphone to start speaking</span>
        )}
      </div>

      <div className="speech-controls">
        <button
          type="button"
          onClick={isListening ? stopListening : startListening}
          className={`mic-button ${isListening ? 'listening' : ''}`}
          disabled={isProcessing}
        >
          {isListening ? (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="6" y="6" width="12" height="12" rx="2" ry="2"></rect>
            </svg>
          ) : (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
              <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
              <line x1="12" y1="19" x2="12" y2="23"></line>
              <line x1="8" y1="23" x2="16" y2="23"></line>
            </svg>
          )}
        </button>

        {transcript && (
          <form onSubmit={handleManualSubmit} className="transcript-form">
            <textarea
              value={transcript}
              onChange={(e) => setTranscript(e.target.value)}
              placeholder="Your speech will appear here..."
              className="transcript-input"
              rows="3"
              disabled={isProcessing}
            />
            <button 
              type="submit" 
              className="submit-transcript"
              disabled={isProcessing || !transcript.trim()}
            >
              {isProcessing ? 'Processing...' : 'Send'}
            </button>
          </form>
        )}
      </div>

      <div className="speech-hint">
        Speak clearly and naturally. The microphone will automatically stop after you finish speaking.
      </div>
    </div>
  );
};

export default SpeechInput;
