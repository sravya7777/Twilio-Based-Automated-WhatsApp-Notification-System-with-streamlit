import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'AC6409ddcce319e4cc67a972c635f0e05d')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '98ba1dde966881a50417891a71f22d5a')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', '+14155238886')

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
