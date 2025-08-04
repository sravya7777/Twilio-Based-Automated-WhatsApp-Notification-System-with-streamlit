#!/usr/bin/env python3
"""
Quick launcher for WhatsApp Message Scheduler
"""

import subprocess
import sys
import os

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import pandas
        import twilio
        import dateutil
        print("✅ All dependencies are available")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def run_streamlit_app():
    """Run the Streamlit app"""
    if not check_dependencies():
        return
    
    print("🚀 Starting WhatsApp Message Scheduler...")
    print("📱 The app will open in your browser at http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the app")
    print("-" * 50)
    
    try:
        # Run the Streamlit app
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"])
    except KeyboardInterrupt:
        print("\n👋 App stopped by user")
    except Exception as e:
        print(f"❌ Error running app: {e}")

if __name__ == "__main__":
    run_streamlit_app() 