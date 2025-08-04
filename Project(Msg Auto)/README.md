# 📱 WhatsApp Message Scheduler

A modern Streamlit web application for scheduling personalized WhatsApp messages using the Twilio API. This app allows you to add multiple recipients, customize messages for each person, and schedule them to be sent at a future date and time.

## ✨ Features

- **Multi-Recipient Support**: Add multiple recipients with custom messages for each
- **Real-time Scheduling**: Schedule messages for future dates and times
- **Input Validation**: Phone number and datetime validation with helpful error messages
- **Status Tracking**: Real-time status updates for sent/failed messages
- **Modern UI**: Responsive design with intuitive user interface
- **Error Handling**: Graceful handling of invalid inputs and API errors

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- Twilio account with WhatsApp API access
- Valid Twilio credentials (Account SID and Auth Token)

### Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Twilio credentials**:
   - Open `streamlit_app.py`
   - Update the `account_sid` and `auth_token` in the `get_twilio_client()` function
   - Ensure your Twilio WhatsApp number is correctly configured

4. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser** and navigate to `http://localhost:8501`

## 📖 Usage Guide

### Adding Recipients

1. **Use the sidebar** to add recipients
2. **Enter recipient details**:
   - Name: The recipient's name
   - Phone Number: WhatsApp number in international format (e.g., +91XXXXXXXXXX)
   - Custom Message: Personalized message for this recipient
3. **Click "Add Recipient"** to save

### Scheduling Messages

1. **Add recipients first** using the sidebar
2. **Select date and time** for when you want messages sent
3. **Click "Schedule Messages"** to confirm scheduling
4. **Monitor status** in the Message Status section

### Managing Recipients

- **View all recipients** in the main table
- **Remove individual recipients** using the remove buttons
- **Clear all recipients** using the sidebar button
- **Edit recipients** by removing and re-adding them

### Message Status

- **⏳ Pending**: Message is scheduled and waiting to be sent
- **✅ Sent**: Message was successfully delivered (includes Twilio SID)
- **❌ Failed**: Message failed to send (includes error details)

## 🔧 Configuration

### Twilio Setup

1. **Create a Twilio account** at [twilio.com](https://www.twilio.com)
2. **Get your credentials**:
   - Account SID
   - Auth Token
3. **Set up WhatsApp messaging**:
   - Configure your Twilio WhatsApp number
   - Ensure proper permissions for sending messages

### Environment Variables (Optional)

For better security, you can use environment variables:

```bash
export TWILIO_ACCOUNT_SID="your_account_sid"
export TWILIO_AUTH_TOKEN="your_auth_token"
```

Then update the `get_twilio_client()` function:

```python
import os

@st.cache_resource
def get_twilio_client():
    account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
    return Client(account_sid, auth_token)
```

## 🛠️ Technical Details

### Architecture

- **Frontend**: Streamlit web interface
- **Backend**: Python with Twilio API integration
- **Scheduling**: Threading-based message scheduling
- **State Management**: Streamlit session state

### Key Components

- **Input Validation**: Phone number and datetime validation
- **Error Handling**: Comprehensive error handling for API calls
- **Real-time Updates**: Status tracking for scheduled messages
- **Responsive Design**: Mobile-friendly interface

### File Structure

```
Project(Msg Auto)/
├── streamlit_app.py      # Main Streamlit application
├── requirements.txt      # Python dependencies
├── main.py             # Original command-line script
└── README.md           # This file
```

## 🔒 Security Notes

- **Never commit credentials** to version control
- **Use environment variables** for production deployments
- **Validate all inputs** to prevent injection attacks
- **Monitor API usage** to stay within Twilio limits

## 🐛 Troubleshooting

### Common Issues

1. **"Invalid phone number" error**:
   - Ensure phone number starts with `+` and country code
   - Example: `+91XXXXXXXXXX` for India

2. **"Scheduled time must be in the future"**:
   - Select a date and time that's after the current time
   - The app prevents scheduling messages in the past

3. **"Failed to send message"**:
   - Check your Twilio credentials
   - Verify your Twilio WhatsApp number is properly configured
   - Ensure recipient numbers are in correct format

4. **App not loading**:
   - Check if all dependencies are installed: `pip install -r requirements.txt`
   - Ensure you're running the correct command: `streamlit run streamlit_app.py`

### Getting Help

- Check the Twilio documentation for API issues
- Review Streamlit documentation for UI problems
- Ensure all dependencies are properly installed

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Note**: This application requires a valid Twilio account with WhatsApp messaging capabilities. Make sure to comply with Twilio's terms of service and WhatsApp's messaging policies. 