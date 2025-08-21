#!/usr/bin/env python3
"""
AI Speech Therapy App - Setup Script
This script helps install all necessary dependencies.
"""

import subprocess
import sys
import os

def install_python_dependencies():
    """Install Python dependencies"""
    print("🔧 Installing Python dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Python dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Python dependencies")
        return False

def install_frontend_dependencies():
    """Install frontend dependencies"""
    print("🔧 Installing frontend dependencies...")
    try:
        frontend_dir = os.path.join(os.getcwd(), "frontend")
        os.chdir(frontend_dir)
        subprocess.run(["npm", "install"], check=True)
        os.chdir("..")
        print("✅ Frontend dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install frontend dependencies")
        return False

def main():
    print("🤖 AI Speech Therapy App - Setup")
    print("=" * 50)
    
    # Check if Python dependencies are needed
    try:
        import flask
        import torch
        import transformers
        import nltk
        print("✅ Python dependencies already installed")
        python_ok = True
    except ImportError:
        print("❌ Python dependencies missing")
        python_ok = False
    
    # Check if frontend dependencies are needed
    if os.path.exists("frontend/node_modules"):
        print("✅ Frontend dependencies already installed")
        frontend_ok = True
    else:
        print("❌ Frontend dependencies missing")
        frontend_ok = False
    
    if python_ok and frontend_ok:
        print("\n🎉 All dependencies are already installed!")
        print("You can now run: python run_app.py")
        return
    
    print("\n🔧 Installing missing dependencies...")
    
    # Install Python dependencies if needed
    if not python_ok:
        if not install_python_dependencies():
            print("❌ Setup failed. Please install Python dependencies manually.")
            return
    
    # Install frontend dependencies if needed
    if not frontend_ok:
        if not install_frontend_dependencies():
            print("❌ Setup failed. Please install frontend dependencies manually.")
            return
    
    print("\n🎉 Setup completed successfully!")
    print("You can now run: python run_app.py")

if __name__ == "__main__":
    main() 