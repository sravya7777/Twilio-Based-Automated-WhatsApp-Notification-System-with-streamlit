import streamlit as st
import pandas as pd
from twilio.rest import Client
from datetime import datetime, timedelta
import time
import threading
from dateutil import parser
import re
import config

# Page configuration
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout=config.PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .recipient-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .status-success {
        color: #28a745;
        font-weight: bold;
    }
    .status-error {
        color: #dc3545;
        font-weight: bold;
    }
    .status-pending {
        color: #ffc107;
        font-weight: bold;
    }
</style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'recipients' not in st.session_state:
    st.session_state.recipients = []
if 'scheduled_messages' not in st.session_state:
    st.session_state.scheduled_messages = []
if 'selected_time' not in st.session_state:
    st.session_state.selected_time = datetime.now().time()
if 'show_success' not in st.session_state:
    st.session_state.show_success = False
if 'success_message' not in st.session_state:
    st.session_state.success_message = ""

# Twilio configuration
@st.cache_resource
def get_twilio_client():
    """Initialize Twilio client with credentials"""
    return Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)

def validate_phone_number(phone):
    """Validate phone number format"""
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', phone)
    # Check if it starts with + and has valid length
    if cleaned.startswith('+') and config.MIN_PHONE_LENGTH <= len(cleaned) - 1 <= config.MAX_PHONE_LENGTH:
        return True, cleaned
    return False, phone

def validate_datetime(date_str, time_str):
    """Validate date and time inputs"""
    try:
        datetime_str = f"{date_str} {time_str}"
        scheduled_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
        current_time = datetime.now()
        
        # Add a small buffer (1 minute) to account for timing differences
        buffer_time = current_time + timedelta(minutes=1)
        
        if scheduled_time <= buffer_time:
            return False, config.ERROR_MESSAGES['past_datetime']
        
        return True, scheduled_time
    except ValueError:
        return False, config.ERROR_MESSAGES['invalid_datetime']

def send_whatsapp_message(recipient, message_body):
    """Send WhatsApp message using Twilio"""
    try:
        print(f"🔍 Attempting to send message to {recipient['name']} at {recipient['number']}")
        print(f"📝 Message: {message_body}")
        print(f"📱 Using WhatsApp number: {config.TWILIO_WHATSAPP_NUMBER}")
        
        client = get_twilio_client()
        message = client.messages.create(
            from_=f'whatsapp:{config.TWILIO_WHATSAPP_NUMBER}',
            body=message_body,
            to=f"whatsapp:{recipient['number']}"
        )
        
        print(f"✅ Message sent successfully! SID: {message.sid}")
        return True, message.sid
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error sending message: {error_msg}")
        
        if "Authenticate" in error_msg or "20003" in error_msg:
            return False, "Twilio authentication failed. Please check your Account SID and Auth Token."
        elif "not found" in error_msg.lower():
            return False, "Twilio WhatsApp number not found. Please verify your WhatsApp number configuration."
        elif "not authorized" in error_msg.lower():
            return False, "Not authorized to send WhatsApp messages. Check your Twilio account permissions."
        else:
            return False, f"Twilio error: {error_msg}"

def check_message_results():
    """Check for message results from background threads"""
    import json
    import os
    import glob
    
    # Check for result files
    result_files = glob.glob('message_result_*.json')
    error_files = glob.glob('message_error_*.json')
    
    for file_path in result_files + error_files:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            # Update session state if we find a matching message
            for msg in st.session_state.scheduled_messages:
                if (msg['recipient']['name'] == data['recipient_name'] and 
                    msg['scheduled_time'].isoformat() == data['scheduled_time']):
                    msg['status'] = data['status']
                    msg['result'] = data['result']
                    break
            
            # Remove the file after processing
            os.remove(file_path)
            
        except Exception as e:
            # If there's an error reading the file, just continue
            continue

def schedule_message(recipient, scheduled_time, custom_message):
    """Schedule a message to be sent at the specified time"""
    def send_scheduled_message():
        try:
            print(f"⏰ Scheduling message for {recipient['name']} at {scheduled_time}")
            
            # Wait until scheduled time
            wait_time = (scheduled_time - datetime.now()).total_seconds()
            print(f"⏳ Waiting {wait_time} seconds...")
            time.sleep(wait_time)
            
            print(f"🚀 Time to send message to {recipient['name']}!")
            
            # Send the message
            message_body = config.DEFAULT_MESSAGE_TEMPLATE.format(
                name=recipient['name'], 
                custom_message=custom_message
            )
            success, result = send_whatsapp_message(recipient, message_body)
            
            # Store result in a file since we can't access session state from thread
            result_data = {
                'recipient_name': recipient['name'],
                'scheduled_time': scheduled_time.isoformat(),
                'status': 'sent' if success else 'failed',
                'result': result,
                'timestamp': datetime.now().isoformat()
            }
            
            # Save to a temporary file
            import json
            with open(f'message_result_{recipient["name"]}_{scheduled_time.strftime("%Y%m%d_%H%M")}.json', 'w') as f:
                json.dump(result_data, f)
                
        except Exception as e:
            # Log error
            error_data = {
                'recipient_name': recipient['name'],
                'scheduled_time': scheduled_time.isoformat(),
                'status': 'failed',
                'result': str(e),
                'timestamp': datetime.now().isoformat()
            }
            import json
            with open(f'message_error_{recipient["name"]}_{scheduled_time.strftime("%Y%m%d_%H%M")}.json', 'w') as f:
                json.dump(error_data, f)
    
    # Start the scheduling thread
    thread = threading.Thread(target=send_scheduled_message)
    thread.daemon = True
    thread.start()

# Main app
def main():
    st.markdown('<h1 class="main-header">📱 WhatsApp Message Scheduler</h1>', unsafe_allow_html=True)
    
    # Check for message results from background threads
    check_message_results()
    
    # Sidebar for adding recipients
    with st.sidebar:
        st.header("➕ Add Recipient")
        
        # Recipient form
        with st.form("recipient_form"):
            name = st.text_input("Name", placeholder="Enter recipient name")
            phone = st.text_input("Phone Number", placeholder="+91XXXXXXXXXX")
            custom_message = st.text_area("Custom Message", placeholder="Enter your message here...")
            
            submitted = st.form_submit_button("Add Recipient")
            
            if submitted:
                if not name or not phone or not custom_message:
                    st.error(config.ERROR_MESSAGES['empty_fields'])
                elif len(custom_message) < config.MIN_MESSAGE_LENGTH or len(custom_message) > config.MAX_MESSAGE_LENGTH:
                    st.error(f"Message must be between {config.MIN_MESSAGE_LENGTH} and {config.MAX_MESSAGE_LENGTH} characters")
                else:
                    # Validate phone number
                    is_valid, cleaned_phone = validate_phone_number(phone)
                    if not is_valid:
                        st.error(config.ERROR_MESSAGES['invalid_phone'])
                    else:
                        recipient = {
                            "name": name,
                            "number": cleaned_phone,
                            "custom_message": custom_message
                        }
                        st.session_state.recipients.append(recipient)
                        st.success(f"✅ Added {name}")
        
        # Display current recipients count
        st.metric("Total Recipients", len(st.session_state.recipients))
        
        # Clear all recipients button
        if st.button("🗑️ Clear All Recipients"):
            st.session_state.recipients = []
            st.success("✅ All recipients cleared!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📋 Recipients List")
        
        # Use a container to make the table more stable
        with st.container():
            if not st.session_state.recipients:
                st.info("No recipients added yet. Use the sidebar to add recipients.")
            else:
                # Display recipients in a table
                recipients_df = pd.DataFrame(st.session_state.recipients)
                st.dataframe(
                    recipients_df,
                    use_container_width=True,
                    hide_index=True
                )
            
            # Remove individual recipients
            st.subheader("Remove Recipients")
            
            # Use a selectbox for removal to avoid dynamic buttons
            if st.session_state.recipients:
                recipient_names = [f"{r['name']} ({r['number']})" for r in st.session_state.recipients]
                selected_recipient = st.selectbox(
                    "Select recipient to remove:",
                    options=recipient_names,
                    key="remove_recipient_select"
                )
                
                if st.button("Remove Selected Recipient", key="remove_button"):
                    # Find the index of the selected recipient
                    for i, recipient in enumerate(st.session_state.recipients):
                        if f"{recipient['name']} ({recipient['number']})" == selected_recipient:
                            removed_name = recipient['name']
                            st.session_state.recipients.pop(i)
                            st.success(f"✅ Removed {removed_name}")
                            break
    
    with col2:
        st.header("⏰ Schedule Messages")
        
        # Help text for time selection
        st.info("💡 **Time Selection**: Choose a future date and time when you want your messages to be sent.")
        
        if not st.session_state.recipients:
            st.warning(config.ERROR_MESSAGES['no_recipients'])
        else:
            # Date and time picker
            col_date, col_time = st.columns(2)
            
            with col_date:
                scheduled_date = st.date_input(
                    "Select Date",
                    min_value=datetime.now().date(),
                    value=datetime.now().date(),
                    help="Select the date when you want to send the messages"
                )
            
            with col_time:
                # Use session state to remember the selected time
                scheduled_time = st.time_input(
                    "Select Time",
                    value=st.session_state.selected_time,
                    key="time_picker",
                    step=300,  # 5-minute intervals
                    help="Select the time when you want to send the messages (24-hour format). Use arrows or type directly."
                )
                # Update session state with the selected time
                st.session_state.selected_time = scheduled_time
            
            # Show selected scheduled time
            selected_datetime = datetime.combine(scheduled_date, scheduled_time)
            current_datetime = datetime.now()
            
            # Display the selected time more prominently
            st.markdown(f"**Selected Time:** {selected_datetime.strftime('%Y-%m-%d %H:%M')}")
            
            # Quick time presets
            st.markdown("**Quick Time Options:**")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("30 min from now"):
                    future_time = datetime.now() + timedelta(minutes=30)
                    st.session_state.selected_time = future_time.time()
            
            with col2:
                if st.button("1 hour from now"):
                    future_time = datetime.now() + timedelta(hours=1)
                    st.session_state.selected_time = future_time.time()
            
            with col3:
                if st.button("2 hours from now"):
                    future_time = datetime.now() + timedelta(hours=2)
                    st.session_state.selected_time = future_time.time()
            
            if selected_datetime > current_datetime:
                st.success(f"✅ This is a future time - messages can be scheduled!")
            else:
                st.warning(f"⚠️ This time is in the past - please select a future time")
                st.info("💡 Tip: Use the time picker above or quick options to select a future time")
            
            # Schedule button
            if st.button("🚀 Schedule Messages", type="primary", use_container_width=True):
                # Validate scheduled time
                is_valid, result = validate_datetime(
                    scheduled_date.strftime("%Y-%m-%d"),
                    scheduled_time.strftime("%H:%M")
                )
                
                if not is_valid:
                    st.error(result)
                else:
                    scheduled_datetime = result
                    
                    # Schedule messages for all recipients
                    for recipient in st.session_state.recipients:
                        scheduled_msg = {
                            "recipient": recipient,
                            "scheduled_time": scheduled_datetime,
                            "custom_message": recipient["custom_message"],
                            "status": "pending",
                            "result": None
                        }
                        st.session_state.scheduled_messages.append(scheduled_msg)
                        
                        # Start scheduling thread
                        schedule_message(recipient, scheduled_datetime, recipient["custom_message"])
                    
                    st.success(f"✅ Messages scheduled for {scheduled_datetime.strftime('%Y-%m-%d %H:%M')}")
                    st.balloons()
                    st.info(f"📱 {len(st.session_state.recipients)} message(s) will be sent automatically at the scheduled time!")
    
    # Display scheduled messages status
    if st.session_state.scheduled_messages:
        st.header("📊 Message Status")
        
        # Auto-refresh status every 5 seconds
        if st.button("🔄 Refresh Status", key="refresh_status"):
            check_message_results()
        
        for i, msg in enumerate(st.session_state.scheduled_messages):
            with st.container():
                col1, col2, col3 = st.columns([2, 2, 1])
                
                with col1:
                    st.markdown(f"**{msg['recipient']['name']}**")
                    st.caption(f"To: {msg['recipient']['number']}")
                
                with col2:
                    st.markdown(f"**Scheduled:** {msg['scheduled_time'].strftime('%Y-%m-%d %H:%M')}")
                    st.caption(f"Message: {msg['custom_message'][:config.MESSAGE_PREVIEW_LENGTH]}...")
                
                with col3:
                    if msg['status'] == 'pending':
                        # Calculate time remaining
                        time_remaining = msg['scheduled_time'] - datetime.now()
                        if time_remaining.total_seconds() > 0:
                            hours = int(time_remaining.total_seconds() // 3600)
                            minutes = int((time_remaining.total_seconds() % 3600) // 60)
                            st.markdown(f'<span class="status-pending">⏳ Pending</span>', unsafe_allow_html=True)
                            st.caption(f"⏰ {hours}h {minutes}m remaining")
                        else:
                            st.markdown(f'<span class="status-pending">⏳ Sending...</span>', unsafe_allow_html=True)
                    elif msg['status'] == 'sent':
                        st.markdown('<span class="status-success">✅ Sent</span>', unsafe_allow_html=True)
                        st.caption(f"SID: {msg['result']}")
                        # Show success popup
                        st.balloons()
                        st.success(f"🎉 Message sent successfully to {msg['recipient']['name']}!")
                    elif msg['status'] == 'failed':
                        st.markdown('<span class="status-error">❌ Failed</span>', unsafe_allow_html=True)
                        st.caption(f"Error: {msg['result']}")
                        st.error(f"❌ Failed to send message to {msg['recipient']['name']}")
                
                st.divider()
        
        # Clear completed messages
        if st.button("🗑️ Clear Completed Messages"):
            st.session_state.scheduled_messages = [
                msg for msg in st.session_state.scheduled_messages 
                if msg['status'] == 'pending'
            ]

if __name__ == "__main__":
    main() 