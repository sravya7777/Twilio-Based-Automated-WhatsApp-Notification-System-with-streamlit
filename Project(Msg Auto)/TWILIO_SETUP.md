# 🔧 Twilio Setup Guide

## Current Issue
You're getting an authentication error (Error 20003) which means your Twilio credentials are either:
- Invalid/expired
- Not properly configured
- Missing proper permissions

## 🔑 Step-by-Step Twilio Setup

### 1. Create/Update Twilio Account

1. **Go to [Twilio Console](https://console.twilio.com/)**
2. **Sign up or log in** to your Twilio account
3. **Navigate to your Dashboard**

### 2. Get Your Credentials

1. **Find your Account SID and Auth Token:**
   - Go to [Console > Dashboard](https://console.twilio.com/)
   - Look for "Account Info" section
   - Copy your **Account SID** and **Auth Token**

2. **Verify your credentials are active:**
   - Make sure your account is not suspended
   - Check that you have sufficient credits

### 3. Set Up WhatsApp Messaging

1. **Enable WhatsApp in your Twilio account:**
   - Go to [Messaging > Try it out > Send a WhatsApp message](https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp)
   - Follow the setup instructions

2. **Get your WhatsApp number:**
   - In the WhatsApp section, you'll see your Twilio WhatsApp number
   - It should look like: `+14155238886`

### 4. Update Your Configuration

**Option A: Update config.py directly**
```python
# In config.py, update these lines:
TWILIO_ACCOUNT_SID = 'your_actual_account_sid_here'
TWILIO_AUTH_TOKEN = 'your_actual_auth_token_here'
TWILIO_WHATSAPP_NUMBER = 'your_actual_whatsapp_number_here'
```

**Option B: Use Environment Variables (Recommended)**
```bash
# Set these environment variables:
export TWILIO_ACCOUNT_SID="your_actual_account_sid"
export TWILIO_AUTH_TOKEN="your_actual_auth_token"
export TWILIO_WHATSAPP_NUMBER="your_actual_whatsapp_number"
```

### 5. Test Your Configuration

Run this test script to verify your credentials:
```bash
python test_twilio_credentials.py
```

## 🚨 Common Issues & Solutions

### Issue 1: "Authenticate" Error (20003)
**Cause:** Invalid Account SID or Auth Token
**Solution:** 
- Double-check your credentials in Twilio Console
- Make sure you're copying the full Account SID and Auth Token
- Verify your account is active and not suspended

### Issue 2: "WhatsApp number not found"
**Cause:** WhatsApp not properly configured
**Solution:**
- Complete the WhatsApp setup in Twilio Console
- Verify your WhatsApp number is active
- Check that you have WhatsApp messaging permissions

### Issue 3: "Not authorized"
**Cause:** Insufficient permissions or account restrictions
**Solution:**
- Upgrade your Twilio account if needed
- Contact Twilio support for WhatsApp permissions
- Verify your account has messaging capabilities

## 🔍 Verification Steps

1. **Check Account Status:**
   - Log into [Twilio Console](https://console.twilio.com/)
   - Verify account is active and has credits

2. **Test Credentials:**
   - Use the test script provided
   - Check if credentials work with a simple API call

3. **Verify WhatsApp Setup:**
   - Ensure WhatsApp messaging is enabled
   - Confirm your WhatsApp number is active

## 📞 Getting Help

- **Twilio Support:** [support.twilio.com](https://support.twilio.com/)
- **Twilio Documentation:** [twilio.com/docs](https://www.twilio.com/docs)
- **WhatsApp Business API:** [twilio.com/whatsapp](https://www.twilio.com/whatsapp)

## ⚠️ Security Notes

- **Never commit real credentials** to version control
- **Use environment variables** for production
- **Rotate your Auth Token** regularly
- **Monitor your usage** to avoid unexpected charges

---

**Next Steps:**
1. Update your credentials in `config.py` or set environment variables
2. Run the test script to verify
3. Try scheduling a message again 