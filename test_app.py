#!/usr/bin/env python3
"""
Test script for AI Speech Therapy App
This script tests the core functionality without starting the full application.
"""

import sys
import os
import signal
import time

def timeout_handler(signum, frame):
    raise TimeoutError("Test timed out")

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    
    try:
        import flask
        print("✅ Flask imported successfully")
    except ImportError as e:
        print(f"❌ Flask import failed: {e}")
        return False
    
    try:
        import torch
        print("✅ PyTorch imported successfully")
    except ImportError as e:
        print(f"❌ PyTorch import failed: {e}")
        return False
    
    try:
        import transformers
        print("✅ Transformers imported successfully")
    except ImportError as e:
        print(f"❌ Transformers import failed: {e}")
        return False
    
    try:
        import nltk
        print("✅ NLTK imported successfully")
    except ImportError as e:
        print(f"❌ NLTK import failed: {e}")
        return False
    
    return True

def test_backend_modules():
    """Test backend module imports"""
    print("\n🔍 Testing backend modules...")
    
    # Add backend to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        from sentiment_model import analyze_with_vader, analyze_with_roberta
        print("✅ Sentiment model imported successfully")
    except ImportError as e:
        print(f"❌ Sentiment model import failed: {e}")
        return False
    
    try:
        from enhanced_response_generator import generate_response
        print("✅ Response generator imported successfully")
    except ImportError as e:
        print(f"❌ Response generator import failed: {e}")
        return False
    
    try:
        from speech_to_text import transcribe_audio
        print("✅ Speech to text imported successfully")
    except ImportError as e:
        print(f"❌ Speech to text import failed: {e}")
        return False
    
    return True

def test_sentiment_analysis():
    """Test sentiment analysis functionality"""
    print("\n🔍 Testing sentiment analysis...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        from sentiment_model import analyze_with_vader, analyze_with_roberta
        
        test_text = "I'm feeling really happy today!"
        
        vader_score = analyze_with_vader(test_text)
        roberta_score = analyze_with_roberta(test_text)
        
        print(f"✅ VADER score: {vader_score}")
        print(f"✅ RoBERTa score: {roberta_score}")
        
        return True
    except Exception as e:
        print(f"❌ Sentiment analysis test failed: {e}")
        return False

def test_response_generation():
    """Test response generation functionality"""
    print("\n🔍 Testing response generation...")
    
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))
    
    try:
        # Set test mode to skip heavy model loading
        os.environ['TEST_MODE'] = 'true'
        
        from enhanced_response_generator import generate_response
        
        test_text = "I'm feeling anxious about my presentation tomorrow"
        
        # Test with dummy sentiment scores
        response = generate_response(0.1, 0.2, test_text)
        
        print(f"✅ Generated response: {response[:100]}...")
        return True
            
    except Exception as e:
        print(f"❌ Response generation test failed: {e}")
        return False

def test_frontend_dependencies():
    """Test if frontend dependencies are available"""
    print("\n🔍 Testing frontend dependencies...")
    
    if not os.path.exists("frontend/package.json"):
        print("❌ Frontend package.json not found")
        return False
    
    if not os.path.exists("frontend/node_modules"):
        print("⚠️  Frontend node_modules not found (run 'cd frontend && npm install')")
        return False
    
    print("✅ Frontend dependencies found")
    return True

def main():
    """Run all tests"""
    print("🤖 AI Speech Therapy App - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Backend Module Tests", test_backend_modules),
        ("Sentiment Analysis Tests", test_sentiment_analysis),
        ("Response Generation Tests", test_response_generation),
        ("Frontend Dependency Tests", test_frontend_dependencies),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} passed")
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The app should work correctly.")
        print("\n🚀 To start the app, run: python start_app.py")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 To fix issues:")
        print("1. Install Python dependencies: pip install -r requirements.txt")
        print("2. Install frontend dependencies: cd frontend && npm install")
        print("3. Run tests again: python test_app.py")

if __name__ == "__main__":
    main() 