from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.mime.text import MIMEText
import base64

# Build the service
service = build('gmail', 'v1', credentials=creds)

# Create the message
message = MIMEMultipart()
text = MIMEText('This is the body of the email')
message.attach(text)

# Encode the message in base64
message_bytes = message.as_bytes()
message_b64 = base64.urlsafe_b64encode(message_bytes).decode()

# Send the message
send_message = {'raw': message_b64}
send_message = (service.users().messages().send(userId="muni.vadlamudi4@gmail.com", body=send_message).execute())

print(F'sent message to {to_email} Message Id: {send_message["id"]}')
