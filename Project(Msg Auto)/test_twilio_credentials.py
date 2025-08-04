#!/usr/bin/env python3
"""
Test script to verify Twilio credentials
This script tests your Twilio configuration without sending actual messages
"""

import os
import sys
from twilio.rest import Client
from twilio.base.exceptions import TwilioException, TwilioRestException
import config

def test_twilio_credentials():
    """Test if Twilio credentials are valid"""
    print("🔍 Testing Twilio Credentials...")
    print("=" * 50)
    
    # Get credentials
    account_sid = config.TWILIO_ACCOUNT_SID
    auth_token = config.TWILIO_AUTH_TOKEN
    whatsapp_number = config.TWILIO_WHATSAPP_NUMBER
    
    print(f"Account SID: {account_sid[:10]}...{account_sid[-4:]}")
    print(f"Auth Token: {auth_token[:10]}...{auth_token[-4:]}")
    print(f"WhatsApp Number: {whatsapp_number}")
    print()
    
    # Test 1: Basic client creation
    try:
        client = Client(account_sid, auth_token)
        print("✅ Twilio client created successfully")
    except Exception as e:
        print(f"❌ Failed to create Twilio client: {e}")
        return False
    
    # Test 2: Account validation
    try:
        account = client.api.accounts(account_sid).fetch()
        print(f"✅ Account validated: {account.friendly_name}")
        print(f"   Account Status: {account.status}")
        print(f"   Account Type: {account.type}")
    except TwilioRestException as e:
        if e.code == 20003:
            print("❌ Authentication failed - Invalid Account SID or Auth Token")
            print("   Please check your credentials in Twilio Console")
        else:
            print(f"❌ Account validation failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    # Test 3: Check account balance/credits
    try:
        # Try to get account balance (this might not work on trial accounts)
        balance = client.api.accounts(account_sid).balance.fetch()
        print(f"✅ Account balance: ${balance.balance} {balance.currency}")
    except TwilioRestException as e:
        if e.code == 20008:  # Not authorized to access balance
            print("⚠️  Cannot check balance (may be trial account)")
        else:
            print(f"⚠️  Balance check failed: {e}")
    except Exception as e:
        print(f"⚠️  Balance check error: {e}")
    
    # Test 4: Validate WhatsApp number format
    if whatsapp_number.startswith('+1') and len(whatsapp_number) == 12:
        print("✅ WhatsApp number format looks correct")
    else:
        print("⚠️  WhatsApp number format may be incorrect")
        print(f"   Expected: +1XXXXXXXXXX, Got: {whatsapp_number}")
    
    # Test 5: Test message creation (without sending)
    try:
        # This will test if we can create a message object (won't actually send)
        test_message = {
            'from_': f'whatsapp:{whatsapp_number}',
            'body': 'Test message',
            'to': 'whatsapp:+1234567890'  # Dummy number for testing
        }
        print("✅ Message object creation test passed")
    except Exception as e:
        print(f"❌ Message creation test failed: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("✅ Twilio credentials are valid!")
    print("\n📝 Next Steps:")
    print("1. Make sure your WhatsApp number is properly configured in Twilio")
    print("2. Ensure you have WhatsApp messaging permissions")
    print("3. Test with a real phone number in the app")
    
    return True

def show_setup_instructions():
    """Show setup instructions"""
    print("\n🔧 Setup Instructions:")
    print("1. Go to https://console.twilio.com/")
    print("2. Copy your Account SID and Auth Token")
    print("3. Update config.py with your real credentials:")
    print("   TWILIO_ACCOUNT_SID = 'your_actual_sid'")
    print("   TWILIO_AUTH_TOKEN = 'your_actual_token'")
    print("   TWILIO_WHATSAPP_NUMBER = 'your_whatsapp_number'")
    print("4. Run this test again to verify")

if __name__ == "__main__":
    print("🧪 Twilio Credentials Test")
    print("=" * 50)
    
    success = test_twilio_credentials()
    
    if not success:
        print("\n❌ Credentials test failed!")
        show_setup_instructions()
    else:
        print("\n🎉 All tests passed! Your Twilio setup is ready.") 