from __future__ import print_function

import base64
import mimetypes
import string
import os
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import google.auth
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.readonly','https://www.googleapis.com/auth/gmail.compose']
def gmail_create_draft_with_attachment():
    #main1()
    """Create and insert a draft email with attachment.
       Print the returned draft's message and id.
      Returns: Draft object, including draft id and message meta data.

      Load pre-authorized user credentials from the environment.
      TODO(developer) - See https://developers.google.com/identity
      for guides on implementing OAuth2 for the application.
    """
    #creds, _ = None
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
            #print(creds)

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='muni.vadlamudi@gmail.com').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(" @#@#@#@#@#@# You are in exception @#@#@#@#@#@#")
        print(f'An error occurred: {error}')
    try:
        # create gmail api client
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='muni.vadlamudi@gmail.com').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])
        mime_message = EmailMessage()
        #print(mime_message)
        # headers
        mime_message['To'] = 'anila.lingutla@gmail.com'
        mime_message['From'] = 'muni.vadlamudi@gmail.com'
        mime_message['Subject'] = 'Test email from python'
        print(mime_message)
        # text
        mime_message.set_content(
            'Hi, this is automated mail with attachment.'
            'Please do not reply.'
        )

        # attachment
        attachment_filename = 'photo1.jpg'
        # guessing the MIME type
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        print(type_subtype)
        maintype, subtype = type_subtype.split('/')
        print(subtype)
        with open(attachment_filename, 'rb') as fp:
            attachment_data = fp.read()
        mime_message.add_attachment(attachment_data, maintype, subtype)
        message_text=' This is test email'
        mime_message = MIMEText(message_text)
        print("$%$%$%$%$%", mime_message)
        #encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()) \
            .decode()
        print("****************", encoded_message)
        # create_draft_request_body = {
        #     'message': {
        #         'raw': encoded_message
        #     }
        # }
        create_message = {
            'raw': encoded_message
        }
        print("after draft", create_message)
        # pylint: disable=E1101
        #draft = service.users().drafts().create(userId="muni.vadlamudi4@gmail.com",body='this is test draft').execute()
        send_message = service.users().messages().send(userId="muni.vadlamudi@gmail.com", body=create_message).execute()
        #draft = service.users().messages().send(userId="muni.vadlamudi@gmail.com", body=create_draft_request_body).execute()
        print("TTTTTTTTTT")
        print(F'Draft id: {send_message["id"]}\nDraft message: {send_message["message"]}')
        print("^^^^^^^^^^^")
    except HttpError as error:
        print(" $$$$$$$$$$$$ You are in exception $$$$$$$$$$$$$$$$$$$$")
        print(F'An error occurred: {error}')
        draft = None
    return send_message


def build_file_part(file):
    print(" !!!!!!!!!! file part !!!!!!!!!!!!!!!!!!!")
    """Creates a MIME part for a file.

    Args:
      file: The path to the file to be attached.

    Returns:
      A MIME part that can be attached to a message.
    """
    content_type, encoding = mimetypes.guess_type(file)

    if content_type is None or encoding is not None:
        content_type = 'application/octet-stream'
    main_type, sub_type = content_type.split('/', 1)
    if main_type == 'text':
        with open(file, 'rb'):
            msg = MIMEText('r', _subtype=sub_type)
    elif main_type == 'image':
        with open(file, 'rb'):
            msg = MIMEImage('r', _subtype=sub_type)
    elif main_type == 'audio':
        with open(file, 'rb'):
            msg = MIMEAudio('r', _subtype=sub_type)
    else:
        with open(file, 'rb'):
            msg = MIMEBase(main_type, sub_type)
            msg.set_payload(file.read())
    filename = os.path.basename(file)
    msg.add_header('Content-Disposition', 'attachment', filename=filename)
    return msg

def main1():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@ check for gamil authontication @@@@@@@@@@@@")
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])
        print("checking for gmail lables &&&&&&&&&&&&&&&&&&&&&&&")
        if not labels:
            print('No labels found.')
            return
        print('Labels:')
        for label in labels:
            print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')

if __name__ == '__main__':
    gmail_create_draft_with_attachment()