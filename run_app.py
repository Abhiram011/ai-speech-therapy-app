#!/usr/bin/env python3
"""
AI Speech Therapy App - Simple Startup Script
Run this to start both backend and frontend servers.
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def run_backend():
    """Start the Flask backend server"""
    print("🚀 Starting AI Speech Therapy Backend...")
    try:
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
        frontend_dir = os.path.join(original_dir, "frontend")
        os.chdir(frontend_dir)
        subprocess.run(["npm", "start"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Shutting down AI Speech Therapy App...")
        print("👋 Thank you for using AI Speech Therapy!")

if __name__ == "__main__":
    main() 