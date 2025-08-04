#!/usr/bin/env python3
"""
Setup script for Twilio credentials
This script helps you configure your Twilio credentials securely
"""

import os
import getpass

def setup_credentials():
    """Interactive setup for Twilio credentials"""
    print("🔧 Twilio Credentials Setup")
    print("=" * 50)
    print("This script will help you configure your Twilio credentials.")
    print("You can get these from: https://console.twilio.com/")
    print()
    
    # Get credentials from user
    account_sid = input("Enter your Twilio Account SID: ").strip()
    auth_token = getpass.getpass("Enter your Twilio Auth Token: ").strip()
    whatsapp_number = input("Enter your Twilio WhatsApp number (e.g., +14155238886): ").strip()
    
    if not account_sid or not auth_token or not whatsapp_number:
        print("❌ All fields are required!")
        return False
    
    # Validate format
    if not account_sid.startswith('AC'):
        print("❌ Account SID should start with 'AC'")
        return False
    
    if len(auth_token) != 32:
        print("❌ Auth Token should be 32 characters long")
        return False
    
    if not whatsapp_number.startswith('+'):
        print("❌ WhatsApp number should start with '+'")
        return False
    
    # Create .env file
    env_content = f"""# Twilio Credentials
TWILIO_ACCOUNT_SID={account_sid}
TWILIO_AUTH_TOKEN={auth_token}
TWILIO_WHATSAPP_NUMBER={whatsapp_number}
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Created .env file with your credentials")
        
        # Update config.py to use environment variables
        config_content = '''import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')

# App Configuration
APP_TITLE = "WhatsApp Message Scheduler"
APP_ICON = "📱"
PAGE_LAYOUT = "wide"

# Validation Settings
MIN_PHONE_LENGTH = 10
MAX_PHONE_LENGTH = 15
MIN_MESSAGE_LENGTH = 1
MAX_MESSAGE_LENGTH = 1000

# UI Settings
MAX_RECIPIENTS_DISPLAY = 50
MESSAGE_PREVIEW_LENGTH = 50
STATUS_UPDATE_INTERVAL = 5  # seconds

# Message Templates
DEFAULT_MESSAGE_TEMPLATE = "Hi {name}, {custom_message}"
ERROR_MESSAGES = {
    'invalid_phone': 'Please enter a valid phone number (e.g., +91XXXXXXXXXX)',
    'invalid_datetime': 'Invalid date or time format',
    'past_datetime': 'Scheduled time must be in the future',
    'empty_fields': 'Please fill in all fields',
    'no_recipients': 'Add recipients first to schedule messages',
    'twilio_error': 'Failed to send message. Check your Twilio credentials.'
}

# Status Messages
STATUS_MESSAGES = {
    'pending': 'Pending',
    'sent': 'Sent',
    'failed': 'Failed'
}

# CSS Classes
CSS_CLASSES = {
    'main_header': 'main-header',
    'status_success': 'status-success',
    'status_error': 'status-error',
    'status_pending': 'status-pending',
    'recipient_card': 'recipient-card'
}
'''
        
        with open('config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        print("✅ Updated config.py to use environment variables")
        
        print("\n📝 Next Steps:")
        print("1. Run: python test_twilio_credentials.py")
        print("2. If test passes, run: streamlit run streamlit_app.py")
        print("3. Add .env to your .gitignore file for security")
        
        return True
        
    except Exception as e:
        print(f"❌ Error saving credentials: {e}")
        return False

if __name__ == "__main__":
    setup_credentials() 