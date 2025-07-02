// RecordAudio.js
import React, { useState, useRef } from 'react';

const RecordAudio = ({ onResult, onStart, addMessage }) => {
  const [recording, setRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [recordingTime, setRecordingTime] = useState(0);
  const [audioURL, setAudioURL] = useState(null);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const timerRef = useRef(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      });
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = (event) => {
        audioChunksRef.current.push(event.data);
      };

      mediaRecorder.onstop = () => {
        const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' });
        const audioUrl = URL.createObjectURL(audioBlob);
        setAudioURL(audioUrl);
        handleAudioSubmit(audioBlob);
      };

      mediaRecorder.start();
      setRecording(true);
      setRecordingTime(0);
      
      // Start timer
      timerRef.current = setInterval(() => {
        setRecordingTime(prev => prev + 1);
      }, 1000);

    } catch (error) {
      console.error('Error starting recording:', error);
      addMessage("System", "Unable to access microphone. Please check your permissions.", 'text');
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && recording) {
      mediaRecorderRef.current.stop();
      setRecording(false);
      
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }

      // Stop all tracks
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
    }
  };

  const handleAudioSubmit = async (audioBlob) => {
    setIsProcessing(true);
    onStart();

    // Add user message to chat
    addMessage("You", "[Audio Message]", 'audio');

    try {
      // Convert audio to WAV format for backend compatibility
      const formData = new FormData();
      formData.append('file', audioBlob, 'recording.webm');

      const response = await fetch('http://127.0.0.1:5001/analyze-audio', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const data = await response.json();
      
      // Update the user message with transcribed text
      addMessage("You", data.transcribed_text, 'audio');
      
      onResult(data);
    } catch (error) {
      console.error('Error processing audio:', error);
      addMessage("System", "Sorry, I'm having trouble processing your audio. Please try again.", 'text');
    } finally {
      setIsProcessing(false);
      setAudioURL(null);
      setRecordingTime(0);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="audio-input-container">
      <div className="audio-status">
        {recording ? (
          <div className="recording-indicator">
            <div className="recording-dot"></div>
            <span>Recording... {formatTime(recordingTime)}</span>
          </div>
        ) : isProcessing ? (
          <div className="processing-indicator">
            <div className="processing-spinner"></div>
            <span>Processing audio...</span>
          </div>
        ) : (
          <span>Click to record your message</span>
        )}
      </div>

      <div className="audio-controls">
        <button
          type="button"
          onClick={recording ? stopRecording : startRecording}
          className={`record-button ${recording ? 'recording' : ''} ${isProcessing ? 'processing' : ''}`}
          disabled={isProcessing}
        >
          {recording ? (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <rect x="6" y="6" width="12" height="12" rx="2" ry="2"></rect>
            </svg>
          ) : (
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <circle cx="12" cy="12" r="10"></circle>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          )}
        </button>

        {audioURL && !isProcessing && (
          <div className="audio-preview">
            <audio controls src={audioURL} className="audio-player">
              Your browser does not support the audio element.
            </audio>
          </div>
        )}
      </div>

      <div className="audio-hint">
        Record a clear audio message. The recording will automatically process when you stop.
      </div>
    </div>
  );
};

export default RecordAudio;
