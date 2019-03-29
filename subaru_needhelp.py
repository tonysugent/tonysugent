#!/usr/bin/python3

import requests
from bs4 import BeautifulSoup as BS
from email.mime.text import MIMEText
import base64
from email.mime.base import MIMEBase
import mimetypes
import os

url = 'https://annarbor.craigslist.org/'
headers = {'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_2 like Mac OS X)'}
response = requests.get(url, headers=headers)

search = url + 'search/sss'

search_params = {'sort': 'rel',
                 'min_price': '50',
                 'query': 'Subaru',
                 'auto_transmission': '1',
                 'srchType': 'T'}


r = requests.get(search, params=search_params, headers=headers)
s = BS(r.content, 'html.parser')
c = s.prettify

price_list = []
title_list = []
loc_list = []
for i,a in enumerate(s.find_all('p', {'class': 'result-info'})):
    price = a.find('span', {'class': 'result-price'}).text
    title = a.find('a', {'class': 'result-title'}).text
    link = a.find('a', attr={'href': ''})

    if i < 20:
        price_list.append(price)
        title_list.append(title)

z = 0

for i in title_list:
    print(title_list[z])
    print(price_list[z])
    z= z+1

class auth:
    def __init__(self,SCOPES,CLIENT_SECRET_FILE, APPLICATION_NAME):
        self.SCOPES = SCOPES
        self.CLIENT_SECRET_FILE = CLIENT_SECRET_FILE
        self.APPLICATION_NAME = APPLICATION_NAME

    def get_credentials(self):
        creds = None

        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server()
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('gmail', 'v1', credentials=creds)

        results = service.users().labels().list(userId='me').execute()
        labels = results.get('labels', [])

        if not labels:
            print('No labels found.')
        else:
            print('Labels:')
            for label in labels:
                print(label['name'])

class send_email:
    def __init__(self, service):
        self.service = service

    def create_message(sender, to , subject, message_text):
        message = MIMEText(message_text)
        message['to'] = to
        message['from'] = sender
        message['subject'] = subject
        return {'raw': base64.urlsafe_b64encode(message.as_bytes())}

    def send_message(self, user_id, message):
            message = (self.service.users().messages().send(userId=user_id, body=message).execute())
            print('Message Id: %s' % message['id'])
            return message

message = send_email.create_message('tony.sugent@gmail.com', 'tony.sugent@gmail.com','Subarus in AA', 'test')
send_email.send_message('me', message)
