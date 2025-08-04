#!/usr/bin/env python3
"""
Test script for WhatsApp Message Scheduler
This script tests the core functionality without sending actual messages
"""

import sys
import os
from datetime import datetime, timedelta
import config

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_phone_validation():
    """Test phone number validation"""
    from streamlit_app import validate_phone_number
    
    test_cases = [
        ("+1234567890", True),
        ("+911234567890", True),
        ("91XXXXXXXXXX", False),  # Missing +
        ("+91", False),  # Too short
        ("+911234567890123456789", False),  # Too long (21 digits)
        ("", False),  # Empty
    ]
    
    print("Testing phone number validation...")
    for phone, expected in test_cases:
        is_valid, cleaned = validate_phone_number(phone)
        status = "✅ PASS" if is_valid == expected else "❌ FAIL"
        print(f"{status}: {phone} -> {is_valid} (expected: {expected})")

def test_datetime_validation():
    """Test datetime validation"""
    from streamlit_app import validate_datetime
    
    now = datetime.now()
    future = now + timedelta(hours=1)
    past = now - timedelta(hours=1)
    near_future = now + timedelta(minutes=30)  # Should pass with buffer
    
    test_cases = [
        (future.strftime("%Y-%m-%d"), future.strftime("%H:%M"), True),
        (near_future.strftime("%Y-%m-%d"), near_future.strftime("%H:%M"), True),
        (past.strftime("%Y-%m-%d"), past.strftime("%H:%M"), False),
        ("invalid", "invalid", False),
    ]
    
    print("\nTesting datetime validation...")
    for date_str, time_str, expected in test_cases:
        is_valid, result = validate_datetime(date_str, time_str)
        status = "✅ PASS" if is_valid == expected else "❌ FAIL"
        print(f"{status}: {date_str} {time_str} -> {is_valid} (expected: {expected})")

def test_config():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    required_configs = [
        'TWILIO_ACCOUNT_SID',
        'TWILIO_AUTH_TOKEN', 
        'TWILIO_WHATSAPP_NUMBER',
        'APP_TITLE',
        'ERROR_MESSAGES'
    ]
    
    for config_name in required_configs:
        if hasattr(config, config_name):
            print(f"✅ {config_name}: OK")
        else:
            print(f"❌ {config_name}: MISSING")

def test_dependencies():
    """Test if all required dependencies are available"""
    print("\nTesting dependencies...")
    
    dependencies = [
        'streamlit',
        'pandas', 
        'twilio',
        'dateutil'
    ]
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep}: OK")
        except ImportError:
            print(f"❌ {dep}: MISSING")

if __name__ == "__main__":
    print("🧪 Testing WhatsApp Message Scheduler")
    print("=" * 50)
    
    test_dependencies()
    test_config()
    test_phone_validation()
    test_datetime_validation()
    
    print("\n" + "=" * 50)
    print("✅ All tests completed!")
    print("\nTo run the app:")
    print("streamlit run streamlit_app.py") 