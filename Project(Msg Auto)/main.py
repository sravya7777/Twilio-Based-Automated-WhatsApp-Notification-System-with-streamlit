from twilio.rest import Client
from datetime import datetime
import time

# Twilio credentials
account_sid = 'AC6409ddcce319e4cc67a972c635f0e05d'
auth_token = '98ba1dde966881a50417891a71f22d5a'
client = Client(account_sid, auth_token)

# Step 1: Collect multiple recipients from user
recipients = []

print("Enter recipient details. Type 'done' as the name when finished.\n")

while True:
    name = input("Enter recipient name: ")
    if name.lower() == "done":
        break
    number = input("Enter recipient WhatsApp number (e.g., +91...): ")
    custom_msg = input("Enter custom message: ")
    recipients.append({
        "name": name,
        "number": number,
        "custom_msg": custom_msg
    })
    print("Recipient added.\n")

if not recipients:
    print("No recipients entered. Exiting.")
    exit()

# Step 2: Get scheduled date and time
date_str = input("Enter the date to send the message (YYYY-MM-DD): ")
time_str = input("Enter the time to send the message (HH:MM in 24-hour format): ")

schedule_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
current_datetime = datetime.now()
delay_sec = (schedule_datetime - current_datetime).total_seconds()

if delay_sec <= 0:
    print("The specified time is in the past. Please enter a future time.")
    exit()

print(f"\nMessages will be sent at {schedule_datetime}...\n")
time.sleep(delay_sec)

# Step 3: Send messages
for recipient in recipients:
    try:
        body = f"Hi {recipient['name']}, {recipient['custom_msg']}"
        message = client.messages.create(
            from_='whatsapp:+14155238886',
            body=body,
            to=f"whatsapp:{recipient['number']}"
        )
        print(f"✅ Message sent to {recipient['name']} (SID: {message.sid})")
    except Exception as e:
        print(f"❌ Failed to send to {recipient['name']}: {e}")
