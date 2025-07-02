#!/usr/bin/env python3
"""
Test script to demonstrate personalized responses
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from enhanced_response_generator import extract_user_details, get_contextual_response, generate_response
from sentiment_model import analyze_with_vader, analyze_with_roberta

def test_personalization():
    """Test various user inputs to see personalized responses"""
    
    test_cases = [
        "I am stressed about the job market",
        "I'm anxious about my upcoming exam",
        "I feel lonely lately",
        "I'm happy about my new relationship",
        "I'm angry at my boss",
        "I'm depressed about my family situation",
        "I'm worried about money",
        "I'm excited about my new job",
        "I feel worthless about my performance at work",
        "I'm having trouble sleeping because of stress"
    ]
    
    print("🧪 Testing Personalized Response System")
    print("=" * 50)
    
    for i, user_input in enumerate(test_cases, 1):
        print(f"\n{i}. User Input: '{user_input}'")
        
        # Extract details
        details = extract_user_details(user_input)
        print(f"   Extracted Details: {details}")
        
        # Get contextual response
        contextual_response = get_contextual_response(user_input)
        if contextual_response:
            print(f"   Contextual Response: {contextual_response}")
        else:
            print("   No contextual response found, using fallback")
        
        # Get full response with sentiment analysis
        vader_score = analyze_with_vader(user_input)
        roberta_score = analyze_with_roberta(user_input)
        full_response = generate_response(vader_score, roberta_score, user_input)
        print(f"   Final Response: {full_response}")
        print("-" * 50)

if __name__ == "__main__":
    test_personalization() 