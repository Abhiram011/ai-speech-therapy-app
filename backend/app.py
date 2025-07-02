from flask import Flask, request, jsonify
from sentiment_model import analyze_with_vader, analyze_with_roberta
from response_generator import generate_response
from speech_to_text import transcribe_audio
import os
import logging

from flask_cors import CORS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


@app.route("/analyze", methods=["POST"])
def analyze_sentiment():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' in request body"}), 400

        user_text = data["text"]
        logger.info(f"Analyzing text: {user_text[:100]}...")

        # Run sentiment analysis
        vader_result = analyze_with_vader(user_text)
        roberta_result = analyze_with_roberta(user_text)

        # Generate AI-powered therapist response
        response = generate_response(
            vader_result,
            roberta_result,
            user_text
        )

        logger.info(f"Generated response: {response[:100]}...")

        return jsonify({
            "text": user_text,
            "vader_result": vader_result,
            "roberta_result": roberta_result,
            "response": response,
            "overall_sentiment": (vader_result + roberta_result) / 2
        })

    except Exception as e:
        logger.error(f"Error in analyze_sentiment: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/analyze-audio", methods=["POST"])
def analyze_audio():
    try:
        if "file" not in request.files:
            return jsonify({"error": "Missing audio file"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        # Save file temporarily
        file_path = "temp_audio.wav"
        file.save(file_path)

        logger.info(f"Processing audio file: {file.filename}")

        # Transcribe speech to text
        text = transcribe_audio(file_path)
        
        if not text or text.strip() == "":
            return jsonify({"error": "Could not transcribe audio to text"}), 400

        logger.info(f"Transcribed text: {text[:100]}...")

        # Run sentiment analysis
        vader_result = analyze_with_vader(text)
        roberta_result = analyze_with_roberta(text)

        # Generate AI-powered therapist response
        response = generate_response(
            vader_result,
            roberta_result,
            text
        )

        # Delete temp file
        if os.path.exists(file_path):
            os.remove(file_path)

        logger.info(f"Generated response: {response[:100]}...")

        return jsonify({
            "transcribed_text": text,
            "vader_result": vader_result,
            "roberta_result": roberta_result,
            "response": response,
            "overall_sentiment": (vader_result + roberta_result) / 2
        })

    except Exception as e:
        logger.error(f"Error in analyze_audio: {str(e)}")
        # Clean up temp file if it exists
        file_path = "temp_audio.wav"
        if os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({"error": "Internal server error"}), 500


@app.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "AI Speech Therapy Backend is running"})


if __name__ == "__main__":
    logger.info("Starting AI Speech Therapy Backend...")
    app.run(debug=True, host="0.0.0.0", port=5001)
