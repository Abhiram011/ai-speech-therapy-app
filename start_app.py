#!/usr/bin/env python3
"""
AI Speech Therapy App - Startup Script
This script helps you start both the backend and frontend servers.
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def check_python_dependencies():
    """Check if Python dependencies are installed"""
    try:
        import flask
        import torch
        import transformers
        import nltk
        print("✅ Python dependencies found")
        return True
    except ImportError as e:
        print(f"❌ Missing Python dependency: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def check_node_dependencies():
    """Check if Node.js dependencies are installed"""
    if not os.path.exists("frontend/node_modules"):
        print("❌ Frontend dependencies missing")
        print("Run: cd frontend && npm install")
        return False
    print("✅ Frontend dependencies found")
    return True

def install_dependencies():
    """Install missing dependencies"""
    print("🔧 Installing dependencies...")
    
    # Install Python dependencies
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False
    
    # Install Node.js dependencies
    try:
        os.chdir("frontend")
        subprocess.run(["npm", "install"], check=True)
        os.chdir("..")
        print("✅ Node.js dependencies installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install Node.js dependencies")
        return False
    
    return True

def run_backend():
    """Start the Flask backend server"""
    print("🚀 Starting AI Speech Therapy Backend...")
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.getcwd(), "backend")
        os.chdir(backend_dir)
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Backend stopped by user")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")

def run_frontend():
    """Start the React frontend server"""
    print("🎨 Starting AI Speech Therapy Frontend...")
    try:
        # Change to frontend directory
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        os.chdir(frontend_dir)
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Frontend stopped by user")
    except Exception as e:
        print(f"❌ Error starting frontend: {e}")

def main():
    print("🤖 AI Speech Therapy App")
    print("=" * 50)
    
    # Check dependencies
    python_ok = check_python_dependencies()
    node_ok = check_node_dependencies()
    
    if not python_ok or not node_ok:
        print("\n❌ Missing dependencies detected.")
        response = input("Would you like to install them now? (y/n): ")
        if response.lower() == 'y':
            if not install_dependencies():
                print("❌ Failed to install dependencies. Please install them manually.")
                return
        else:
            print("❌ Please install missing dependencies before starting the app.")
            return
    
    print("\n🎯 Starting AI Speech Therapy App...")
    print("📱 Backend: http://localhost:5001")
    print("🌐 Frontend: http://localhost:3000")
    print("⏹️  Press Ctrl+C to stop both servers")
    print("=" * 50)
    
    # Store the original directory
    original_dir = os.getcwd()
    
    # Start backend in a separate thread
    backend_thread = Thread(target=run_backend, daemon=True)
    backend_thread.start()
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Open browser
    try:
        webbrowser.open("http://localhost:3000")
    except:
        pass
    
    # Start frontend in main thread
    try:
        # Change to frontend directory for main thread
        frontend_dir = os.path.join(original_dir, "frontend")
        os.chdir(frontend_dir)
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AI Speech Therapy App...")
        print("👋 Thank you for using AI Speech Therapy!")

if __name__ == "__main__":
    main() 