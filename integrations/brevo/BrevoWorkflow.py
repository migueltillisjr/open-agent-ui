#!/usr/bin/env python3.11
import shutil
import os
import pytz
import inspect
from pathlib import Path
import sys
from datetime import datetime, timedelta, timezone
import requests
import json
import time
import uuid
from .MakeRequest import make_request, brevo_load_contacts, adhoc_brevo_load_contacts

global headers
global folder_id
global contact_list_name
global contact_list_id
global folder_name
global contacts
global campaign_name
global campaigns

config = object()

current_directory = os.path.dirname(os.path.abspath(__file__))
with open(f'{current_directory}/config.json', 'r') as file:
    config = json.load(file)
folder_name=config['folder_name']
contact_list_name=config['contact_list_name']
campaign_name=config['campaign_name']

fqdn = os.getenv('HOST')
port = os.getenv('REPORT_ACCESS_PORT')
app_files = os.getenv('APP_FILES')

API_KEY='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'
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'api-key': API_KEY,
  'Cookie': '__cf_bm=m0D5f_XED4_fm_jlOIpAAi6abzAK2gJhwuDm7yObxfE-1708200064-1.0-AWSVKuZT6T5DFUXvTHhyY6p1CQm3mZpQfFxyQYOSwoS5MC8hpZ0LowZMOHa6RZyrqaE+SElN6+1QpKXXk3JAtvw='
}

def date_now():
    # Get the current date and time in UTC
    current_datetime = datetime.now(pytz.utc)
    # Add 1 minute to the current time
    current_datetime_plus_1min = current_datetime + timedelta(minutes=1)
    # Format the datetime object as a string
    date_str = current_datetime_plus_1min.strftime('%Y-%m-%dT%H:%M:%S')
    return date_str


def date_translate(date_str: str):
    # Parse year, month, and day components
    year = int(date_str[:4])
    month = int(date_str[4:6])
    day = int(date_str[6:8])

    # Get the current time in UTC
    current_time_utc = datetime.utcnow().replace(tzinfo=pytz.utc)

    # Add 5 minutes to the current time
    future_time_utc = current_time_utc + timedelta(minutes=5)

    # Set the date to the parsed date
    future_time_utc = future_time_utc.replace(year=year, month=month, day=day)

    # Format the future time to RFC3339 format
    rfc3339_future_time = future_time_utc.isoformat()

    return rfc3339_future_time


def naming_date():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the datetime object as a string with the desired format
    formatted_date = current_datetime.strftime('%Y%d%m-%H%M%S')
    return formatted_date


def create_campaign_schedule_file(file_name, campaign_data):
    with open(file_name, "w") as file:
        # Write content to the file
        file.write(campaign_data)

def copy_contacts(user_id, file_name):
    shutil.copy(f"{app_files}/users/{user_id}/user_contacts.csv", file_name)


def create_campaign_email_template_file(user_id, file_name):
    shutil.copy(f"{app_files}/users/{user_id}/email-design.html", file_name)


def save_campaign(user_id, data: object) -> object:
    # Create campaign name
    campaign_name = f"{data['scheduledAt']}-E3-Campaign"
    url = "https://api.brevo.com/v3/emailCampaigns"

    # Create campaign email
    # Copy the current existing configured email template using the tool
    # https://SERVER/uploads/tiny-mice.html
    create_campaign_email_template_file(user_id=user_id, file_name=f'{app_files}/users/{user_id}/email_designs/{campaign_name}.html')

    # Copy over user provided contacts uploads/user_contacts.csv
    # that was uploaded in the previous SERVER/upload_contacts POST API request from the view /index.php
    #copy_contacts(f'/var/www/html/uploads/contacts/{campaign_name}.csv')

    # Load contacts into new Brevo contact list and retrieve list ID for the scheduling payload
    list_id = adhoc_brevo_load_contacts(user_id=user_id, adhoc_contacts=True, file_path=f'{app_files}/users/{user_id}/contacts/{campaign_name}.csv', list_name=campaign_name)
    print("LIST ID")
    print(list_id)

    payload = json.dumps({
        "tag": 'E3-Campaign',
        "sender": {
            #"name": data['sender_name'], 
            "email": 'no-reply@ldmg.org'}, 
            "name": f'{campaign_name}',
            "htmlUrl": f'http://{fqdn}:{port}/email_designs/{campaign_name}.html',
            "scheduledAt": date_translate(data['scheduledAt']),
            "subject": data['subject'],
            "replyTo": 'no-reply@ldmg.org',
            "toField": '{{contact.NAME}}',
            "recipients": {
                #"listIds": [int(contact_list_id(contact_lists(), data['test']))]
                "listIds": [int(list_id)]
                },
            #"attachmentUrl": 'https://attachment.domain.com/myAttachmentFromUrl.jpg',
            "inlineImageActivation": False,
            "mirrorActive": False,
            "recurring": False,
            "type": 'classic',
            "header": 'If you are not able to see this mail, click {here}',
            "footer": 'If you wish to unsubscribe from our newsletter, click {here}',
            "params": {'PARAMETER': 'My param value' , 'ADDRESS': 'Seattle, WA', 'SUBJECT': 'New Subject'},
      }, indent=4)
    # Create the file containing the Brevo payload to be used for running the campaign using /etc/crontab entry
    # */5 * * * * root /usr/bin/bash -c "cd /var/www/html/;/usr/local/bin/python3.11 -c \"from BrevoSend import schedule_campaign;schedule_campaign()\"
    create_campaign_schedule_file(f'{app_files}/users/{user_id}/campaigns/{campaign_name}', payload)


def adhoc_build_campaign(user_id, data: object):
    # if a test don't load contacts
    if 'test' in data.keys():
        if data['test'] == 'yes':
            save_campaign(user_id, data)
    else:
        # If the test key is not defined send as a test by default
        data['test'] = 'yes'
        save_campaign(user_id, data)


if __name__ == "__main__":
    data = {
        "test": "yes",
        "sender_name": "Miguel",
        "scheduledAt": "20240422",
        "subject": "sample subject",
    }
    adhoc_build_campaign(data)



