import base64
import os.path
import mimetypes
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Load previously obtained credentials from token.json
creds = None
if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open("token.json", "w") as token:
        token.write(creds.to_authorized_user_info())

service = build("gmail", "v1", credentials=creds)

sender = 'muni.vadlamudi47@gmail.com'
to = ['muni.vadlamudi47@gmail.com'] #,'vnswamy6@gmail.com','vikramkambhoji@gmail.com','sitaramchowdaryunnam@gmail.com','sreedhar.siddam@gmail.com']
bcc = ['vnswamy6@gmail.com']#,'vikramkambhoji@gmail.com','sitaramchowdaryunnam@gmail.com','sreedhar.siddam@gmail.com']
subject = f"Daily Buy Report - {datetime.now().strftime('%Y-%m-%d')}"
message_text = "Please check the attached report for daily analysis. \n This is purely for educational and personal viewing, and not a recommendation for purchasing."
file_path = 'C:/Users/muniv/Desktop/Market/marketdata_analysis/Buy_Entry.csv' #,'C:/Users/muniv/Desktop/Market/marketdata_analysis/Sell_Entry.csv']  # Replace with your attachment file path
def create_message_with_attachment(sender, to, bcc, subject, message_text, file_path):
    message = MIMEMultipart()
    message["to"] = to
    message["bcc"] = bcc
    message["subject"] = subject

    msg = MIMEText(message_text)
    message.attach(msg)

    content_type, encoding = mimetypes.guess_type(file_path)
    if content_type is None or encoding is not None:
        content_type = "application/octet-stream"
    main_type, sub_type = content_type.split("/", 1)
    with open(file_path, "rb") as attachment:
        part = MIMEBase(main_type, sub_type)
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {os.path.basename(file_path)}",
    )
    message.attach(part)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw_message}

# Set the 'to' field directly in the message dictionary
message = create_message_with_attachment(sender, ', '.join(to), ', '.join(bcc) ,subject, message_text, file_path)

try:
    sent_message = (
        service.users().messages().send(userId="me", body=message).execute()
    )
    print(f"Sent message Message Id: {sent_message['id']}")
except HttpError as error:
    print(f"An error occurred: {error}")
