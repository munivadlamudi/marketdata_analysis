import os
import pandas as pd
import base64
import pickle
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# Load your existing report CSV file
report_file = 'C:/Users/mvadlamudi/Desktop/activity/QuantAnalysis/Reports_gen_multi_d25-08-2023__Test_with_URL.csv'
df = pd.read_csv(report_file)

# Convert 'Entry Date' to datetime format
df['Entry Date'] = pd.to_datetime(df['Entry Date'])

# Sort dataframe by 'Entry Date'
df_sorted = df.sort_values('Entry Date')

# Get the unique dates and select the last two
unique_dates = df_sorted['Entry Date'].unique()
last_two_dates = unique_dates[-2:]

# Filter DataFrame to include only rows where 'Entry Type' is 'Golden entry' 
# and 'Entry Date' is within the last two unique dates
df_filtered = df_sorted[(df_sorted['Entry Type'] == 'Golden entry') & (df_sorted['Entry Date'].isin(last_two_dates))]

# Sort the filtered DataFrame in descending order by 'Entry Date'
df_filtered = df_filtered.sort_values('Entry Date', ascending=False)

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Load previously obtained credentials from token.pickle
creds = None
if os.path.exists("token.pickle"):
    with open("token.pickle", 'rb') as token:
        creds = pickle.load(token)

# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)

    # Save the credentials for the next run
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)

service = build("gmail", "v1", credentials=creds)

sender = 'muni.vadlamudi47@gmail.com'
to = ['muni.vadlamudi47@gmail.com'] 
bcc = ['muni.vadlamudi47@gmail.com']
subject = f"Daily Report - {datetime.now().strftime('%Y-%m-%d')}"
message_text = "Please check the attached report for daily analysis. \n This is purely for educational and personal viewing, and not a recommendation for purchasing."

def create_message_with_df(sender, to, bcc, subject, message_text, df):
    # Convert the DataFrame to HTML
    df_html = df.to_html()

    # Create the email message
    message = MIMEMultipart()
    message["to"] = to
    message["bcc"] = bcc
    message["subject"] = subject

    # Create the email body
    msg = MIMEText(f"{message_text}\n\n{df_html}", "html")
    message.attach(msg)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
    return {"raw": raw_message}

# Set the 'to' field directly in the message dictionary
message = create_message_with_df(sender, ', '.join(to), ', '.join(bcc) ,subject, message_text, df_filtered)

try:
    sent_message = (
        service.users().messages().send(userId="me", body=message).execute()
    )
    print(f"Sent message Message Id: {sent_message['id']}")
except HttpError as error:
    print(f"An error occurred: {error}")