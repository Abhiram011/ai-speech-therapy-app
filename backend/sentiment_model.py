import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from transformers import pipeline

# Ensure NLTK resources are downloaded
nltk.download("vader_lexicon")

# Initialize analyzers
vader_analyzer = SentimentIntensityAnalyzer()

# Use a specific model to avoid Keras compatibility issues
try:
    roberta_pipeline = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest")
except Exception as e:
    # Warning: Could not load RoBERTa model: {e}
    # Will use VADER sentiment analysis only
    roberta_pipeline = None

def analyze_with_vader(text):
    """Returns the compound sentiment score using NLTK's VADER."""
    score = vader_analyzer.polarity_scores(text)
    return score["compound"]

def analyze_with_roberta(text):
    """Returns +1 for positive, -1 for negative, 0 for neutral using RoBERTa."""
    if roberta_pipeline is None:
        # Fallback to VADER if RoBERTa is not available
        vader_score = analyze_with_vader(text)
        if vader_score > 0.1:
            return 1
        elif vader_score < -0.1:
            return -1
        else:
            return 0
    
    try:
        result = roberta_pipeline(text)[0]
        label = result["label"]

        if label == "POSITIVE":
            return 1
        elif label == "NEGATIVE":
            return -1
        else:
            return 0
    except Exception as e:
        # RoBERTa analysis failed: {e}
        # Fallback to VADER
        vader_score = analyze_with_vader(text)
        if vader_score > 0.1:
            return 1
        elif vader_score < -0.1:
            return -1
        else:
            return 0
