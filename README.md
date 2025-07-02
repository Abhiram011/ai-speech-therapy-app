# 🤖 AI Speech Therapy App

A comprehensive AI-powered speech therapy application that provides personalized therapeutic responses using advanced pattern matching and AI-powered fallback responses.

![AI Speech Therapy App](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge&logo=robot)
![React](https://img.shields.io/badge/React-19.1.0-blue?style=for-the-badge&logo=react)
![Python](https://img.shields.io/badge/Python-3.12-green?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.3.3-red?style=for-the-badge&logo=flask)

## ✨ Features

### 🧠 **Intelligent Response System**
- **Pattern Matching**: Recognizes 50+ mental health topics and emotional states
- **Personalized Responses**: Incorporates user's specific words and context
- **AI Fallback**: Uses Blenderbot-400M-distill for additional responses when needed
- **Quality Filtering**: Ensures only high-quality, therapeutic responses are used
- **Sentiment-Aware**: Analyzes emotional content using VADER and RoBERTa models

### 🎤 **Multiple Input Methods**
- **Text Input**: Direct text entry for quick communication
- **Voice-to-Text**: Real-time speech recognition using Web Speech API
- **Audio Recording**: Record and upload audio files for analysis
- **Cross-platform Support**: Works on desktop and mobile browsers

### 🧠 **Advanced Sentiment Analysis**
- **Dual Model Approach**: Combines VADER (lexicon-based) and RoBERTa (neural) analysis
- **Emotional Intelligence**: Understands context and emotional nuances
- **Personalized Responses**: Tailors responses based on detected sentiment

### 🎨 **Modern UI/UX**
- **Responsive Design**: Beautiful, modern interface that works on all devices
- **Real-time Feedback**: Visual indicators for processing and listening states
- **Smooth Animations**: Professional chat interface with smooth transitions
- **Accessibility**: Designed with accessibility in mind

### 🔒 **Privacy & Security**
- **Local Processing**: AI responses generated locally
- **No Data Storage**: Conversations are not stored
- **Secure Communication**: HTTPS-ready backend
- **MIT Licensed**: Free to use and modify

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- npm or yarn

### One-Command Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Abhiram011/ai-speech-therapy-app.git
   cd ai-speech-therapy-app
   ```

2. **Start the application**
   ```bash
   python start_app.py
   ```
   
   This will:
   - Check for dependencies
   - Install missing packages if needed
   - Start both backend and frontend servers
   - Open the app in your browser

### Manual Setup (Alternative)

1. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

3. **Start the backend**
   ```bash
   cd backend
   python app.py
   ```

4. **Start the frontend** (in another terminal)
   ```bash
   cd frontend
   npm start
   ```

The app will be available at: `http://localhost:3000`

## 📱 How to Use

### 1. **Text Input** ✏️
- Click the "Type" tab
- Write your thoughts and feelings in the text area
- Press Enter or click "Send"
- Receive personalized therapeutic response

### 2. **Voice Input** 🎙️
- Click the "Voice" tab
- Click the microphone button
- Speak clearly and naturally
- The app will transcribe and analyze your speech
- Receive therapeutic response

### 3. **Audio Recording** 🎤
- Click the "Record" tab
- Click the record button to start
- Speak your message
- Click stop when finished
- Audio will be processed and transcribed
- Receive AI response

## 🏗️ Architecture

### Backend (Python/Flask)
```
backend/
├── app.py                        # Main Flask application
├── enhanced_response_generator.py # Intelligent response system
├── sentiment_model.py            # Sentiment analysis
└── speech_to_text.py             # Audio transcription
```

### Frontend (React)
```
frontend/src/
├── App.js                 # Main application component
├── components/
│   ├── TextInput.js       # Text input component
│   ├── SpeechInput.js     # Voice-to-text component
│   ├── RecordAudio.js     # Audio recording component
│   └── ResultBox.js       # Response display component
└── App.css               # Modern styling
```

## 🤖 AI Models Used

### **Blenderbot-400M-distill**
- **Purpose**: Generate additional AI responses when pattern matching doesn't apply
- **License**: MIT (Free for commercial use)
- **Features**: Conversational AI, empathetic responses
- **Quality Filtering**: Only high-quality responses are used

### **Sentiment Analysis**
- **VADER**: Rule-based sentiment analysis
- **RoBERTa**: Transformer-based sentiment analysis
- **Combined**: Enhanced accuracy through ensemble approach

## 🔧 API Endpoints

### Text Analysis
```http
POST /analyze
Content-Type: application/json

{
  "text": "I'm feeling anxious about my presentation tomorrow"
}
```

### Audio Analysis
```http
POST /analyze-audio
Content-Type: multipart/form-data

file: audio_file.wav
```

### Health Check
```http
GET /health
```

## 🎨 Customization

### Modifying Response Patterns
Edit `backend/enhanced_response_generator.py`:
- Add new topic keywords in `extract_user_details()`
- Add new response templates in `get_contextual_response()`
- Adjust AI model parameters
- Modify therapeutic prompts

### Styling Changes
Edit `frontend/src/App.css`:
- Modify color schemes
- Adjust animations
- Change layout dimensions
- Customize responsive breakpoints

## 🚀 Deployment

### Backend Deployment
```bash
# Using Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 backend.app:app
```

### Frontend Deployment
```bash
cd frontend
npm run build
# Deploy the build/ folder to your hosting service
```

## 🛠️ Development

### Project Structure
```
ai-speech-therapy-app/
├── backend/              # Flask backend
├── frontend/             # React frontend
├── requirements.txt      # Python dependencies
├── start_app.py         # Main startup script
├── test_app.py          # Test suite
├── test_personalization.py # Response testing
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

### Running Tests
```bash
# Run the test suite
python test_app.py

# Test personalized responses
python test_personalization.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This application is for educational and research purposes only. It is not a substitute for professional mental health care. If you are experiencing a mental health crisis, please contact a licensed mental health professional or call your local emergency services.

## 🙏 Acknowledgments

- Hugging Face for the transformer models
- React team for the frontend framework
- Flask team for the backend framework
- All contributors and users of this project

---

**Made with ❤️ for mental health and emotional support**
