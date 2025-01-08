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
from .MakeRequest import brevo_load_contacts, make_request

fqdn = os.getenv('HOST')
host = fqdn
port = os.getenv('REPORT_ACCESS_PORT')

global headers
global folder_id
global contact_list_name
global contact_list_id
global folder_name
global contacts
global campaign_name
global campaigns

current_directory = os.path.dirname(os.path.abspath(__file__))

config = object()
with open(f'{current_directory}/config.json', 'r') as file:
    config = json.load(file)
folder_name=config['folder_name']
contact_list_name=config['contact_list_name']
campaign_name=config['campaign_name']
app_files = os.getenv('APP_FILES')


API_KEY='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'
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'api-key': API_KEY,
  'Cookie': '__cf_bm=m0D5f_XED4_fm_jlOIpAAi6abzAK2gJhwuDm7yObxfE-1708200064-1.0-AWSVKuZT6T5DFUXvTHhyY6p1CQm3mZpQfFxyQYOSwoS5MC8hpZ0LowZMOHa6RZyrqaE+SElN6+1QpKXXk3JAtvw='
}


def list_campaigns() -> object:
    global campaigns
    print("LISTING_CAMPAIGNS")
    url = "https://api.brevo.com/v3/emailCampaigns"
    payload = json.dumps({})
    campaigns = make_request("GET", payload, url)['campaigns']
    return campaigns


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


def contact_lists() -> object:
    url = "https://api.brevo.com/v3/contacts/lists"
    return make_request("GET", {}, url)["lists"]


def contact_list_id(contact_lists, __test) -> object:
    if __test.lower() == "yes":
        for item in contact_lists:
            if 'E3Test2' == item["name"]:
                print(f"Contact list id is {item['id']}")
                return item["id"]
    else:
        for item in contact_lists:
            if contact_list_name == item["name"]:
                print(f"Contact list id is {item['id']}")
                return item["id"]
    return None


def create_email_template(subject: str):
    url="https://api.brevo.com/v3/smtp/templates"
    payload = json.dumps({
        "templateName": "E3-Email-Template",
        "sender": {
            "name": "noreply",
            "email": "noreply@ldm-group.org"
        },
        "htmlUrl": f"http://{host}:{port}/email-design.html",
        "subject": subject,
        "replyTo": "noreplyto@ldm-group.org",
        "toField": "example@example.com",
        "isActive": True
    })
    return make_request("POST", payload, url)['id']


def create_campaign_schedule_file(file_name, campaign_data):
    with open(file_name, "w") as file:
        # Write content to the file
        file.write(campaign_data)


def get_campaign_schedule_file_data(file_name):
    campaign_data = dict()
    with open(file_name, "r") as file:
        campaign_data = json.load(file)
    return campaign_data


def send_campaign(filename: str) -> object:
    print("Sending Campaign...")
    url = "https://api.brevo.com/v3/emailCampaigns"
    payload = get_campaign_schedule_file_data(f'{app_files}/users/{user_id}/campaigns/{filename}')
    payload['scheduledAt'] = date_now()
    payload = json.dumps(payload, indent=4)
    resp = make_request("POST", payload, url)
    os.remove(f'{app_files}/users/{user_id}/campaigns/{filename}')
    print(f"File {app_files}/users/{user_id}/campaigns/{filename} removed successfully.")
    return resp


def get_email_template():
    email_data=str()
    with open(f"{app_files}/users/{user_id}/email-design.html", "r") as file:
        email_data = file.read()
    return email_data


def create_campaign_email_template_file(file_name):
    shutil.copy(f"{app_files}/users/{user_id}/email-design.html", file_name)


def save_campaign(data: object) -> object:
    url = "https://api.brevo.com/v3/emailCampaigns"
    create_campaign_email_template_file(f'{app_files}/users/{user_id}/campaigns/{data["scheduledAt"]}-E3-Campaign.html')
    payload = json.dumps({
        "tag": 'E3-Campaign',
        #"sender": {"name": data['sender_name'], "email": 'noreply@ldm-group.org'}, "name": f'{data["scheduledAt"]}-E3-Campaign',
        "sender": {"name": data['sender_name'], "email": 'zoila@ldmg.org'}, "name": f'{data["scheduledAt"]}-E3-Campaign',
        "htmlUrl": f'http://{host}:{port}/uploads/email_designs/{data["scheduledAt"]}-E3-Campaign.html',
        #"templateId": create_email_template(data['subject']),
        "scheduledAt": date_translate(data['scheduledAt']),
        "subject": data['subject'],
        "replyTo": 'noreply@ldm-group.org',
        "toField": '{{contact.NAME}}',
        "recipients": {"listIds": [int(contact_list_id(contact_lists(), data['test']))]},
        #"attachmentUrl": 'https://attachment.domain.com/myAttachmentFromUrl.jpg',
        "inlineImageActivation": False,
        "mirrorActive": False,
        "recurring": False,
        "type": 'classic',
        "header": 'If you are not able to see this mail, click {here}',
        "footer": 'If you wish to unsubscribe from our newsletter, click {here}',
        #"utmCampaign": 'My utm campaign value',
        "params": {'PARAMETER': 'My param value' , 'ADDRESS': 'Seattle, WA', 'SUBJECT': 'New Subject'},
        #"htmlContent": json.dumps(get_email_template()).replace('\\n', '')[1:-1]
      }, indent=4)
    create_campaign_schedule_file(f'{app_files}/users/{user_id}/campaigns/{data["scheduledAt"]}-E3-Campaign', payload)


def delete_scheduled_campaign(campaign_id: str, campaign_name: str):
    pass


def return_campaign_files(user_id: str):
    # Path to the 'campaigns' directory
    campaigns_dir = Path(f'{app_files}/users/{user_id}/campaigns')
    # List comprehension to get file names in the directory
    campaign_files = [file.name for file in campaigns_dir.iterdir() if file.is_file()]
    # Print or return the list of campaign files
    return campaign_files


def delete_campaign_files(user_id: str, filenames_to_delete: list):
    campaigns_dir = f'{app_files}/users/{user_id}/campaigns'
    files_in_dir = os.listdir(campaigns_dir)
    # Check if there are any files in the directory
    if files_in_dir:
        # Iterate over each file in the directory
        for file_name in files_in_dir:
            file_name = file_name.replace(' - ', '')
            file_path = os.path.join(campaigns_dir, file_name)
            # Check if the file is a file (and not a directory) and its name is in the list
            if os.path.isfile(file_path) and file_name in filenames_to_delete:
                # Delete the file
                os.remove(file_path)
                print(f"Deleted: {file_path}")
        return "Campaigns deleted"
    else:
        print("No files found in the directory.")
        return "No campaigns found"


#def suspend_brevo_campaign(campaign_name: str):
#    cs = list()
#    #url = "https://api.brevo.com/v3/emailCampaigns"
#    url = "https://api.brevo.com/v3/emailCampaigns?status=queued&excludeHtmlContent=true"
#    payload = json.dumps({}, indent=4)
#    campaigns = make_request("GET", payload, url)['campaigns']
#    for c in campaigns:
#        cs.append(c['name'])
#    return cs


def schedule_campaign(user_id) -> object:
    # Define the directory to check
    directory = f"{app_files}/users/{user_id}/campaigns"
    
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
    else:
        # List all files in the directory
        files = os.listdir(directory)
        if not files:
            print("No files found in the directory.")
        else:
            # Get the current GMT time
            current_gmt = datetime.now(timezone.utc)
    
            for filename in files:
                #print(filename)
                # Extract the creation date from the file name (format "YYYYMMDD-...")
                try:
                    file_date_str = filename.split('-')[0]
                    file_date = datetime.strptime(file_date_str, "%Y%m%d").replace(tzinfo=timezone.utc)
                    
                    # Compare the file's creation date with the current GMT time
                    # But don't send on the same day
                    if file_date < current_gmt:
                        # Do something if the file's creation date is before the current GMT time
                        print(f"File '{filename}' is before the current GMT time. Do something.")
                        print(filename)
                        file_path = os.path.join(directory, filename)
                        try:
                            with open(file_path, 'r') as file:
                                data = json.load(file)
                                send_campaign(filename)
                                #os.remove(directory + "/" + filename)
                        except Exception as e:
                            print(f"Failed to read or parse '{filename}': {e}")

                    else:
                        # Do nothing if the file's creation date is not before the current GMT time
                        print(filename)
                        print(f"File '{filename}' is not before the current GMT time. Do nothing.")
                except ValueError:
                    print(f"Filename '{filename}' does not conform to the expected format. Skipping.")


def get_campaign_report(c_id: str):
    url=f"https://api.brevo.com/v3/emailCampaigns/{c_id}"
    payload = json.dumps({})
    return make_request("GET", payload, url)


def recent_campaign_reports():
    time.sleep(5)
    list_campaigns()
    c = [{"id": item['id'], "name": item['name'], "status": item['status']} for item in campaigns if 'Notify-E3' not in item['name']]
    c = sorted(c, key=lambda x: x['id'], reverse=True)
    #c = c[0:5]
    for item in c:
        report = get_campaign_report(item['id'])
        del report['htmlContent']
        item['report'] = report
    return c


def build_campaign(data: object):
    # if a test don't load contacts
    if 'test' in data.keys():
        if data['test'] == 'yes':
            list_campaigns()
            save_campaign(data)
            create_email_template(data['subject'])
    else:
        # If the test key is not defined send as a test by default
        data['test'] = 'yes'
        list_campaigns()
        save_campaign(data)
        create_email_template(data['subject'])


if __name__ == "__main__":
    #list_campaigns()
    data = {
        "test": "yes",
        "sender_name": "Miguel",
        "scheduledAt": "20240330",
        "subject": "sample subject",
    }
    build_campaign(data)
    data = {
        "test": "yes",
        "sender_name": "Miguel",
        "scheduledAt": "20240322",
        "subject": "sample subject",
    }
    build_campaign(data)
    #schedule_campaign()
    #delete_campaign_files(return_campaign_files())



