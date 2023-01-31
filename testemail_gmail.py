from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def send_email(to, body):
    try:
        service = build('gmail', 'v1', credentials=credentials)
        message = create_message(to, body)
        send_message(service, "me", message)
        print(F'sent email to {to}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        print('Email not sent')

def create_message(to, body):
    message = MIMEMultipart()
    text = MIMEText(body)
    message.attach(text)
    message['to'] = to
    message['subject'] = 'Subject of your email'
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print(F'Email was sent to {to} Message Id: {message["id"]}')
    except HttpError as error:
        print(F'An error occurred: {error}')
        print("Email not sent")

credentials = Credentials.from_authorized_user_info(info=info)
send_email("receiver@gmail.com", "Your message here")
