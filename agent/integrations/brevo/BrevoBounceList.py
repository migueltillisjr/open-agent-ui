#!/usr/bin/env python3.11
import os
import urllib.parse
import pytz
from datetime import datetime, timedelta, timezone
import json
from .MakeRequest import make_request

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
app_files = os.getenv('APP_FILES')

API_KEY='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'
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'api-key': API_KEY,
  'Cookie': '__cf_bm=m0D5f_XED4_fm_jlOIpAAi6abzAK2gJhwuDm7yObxfE-1708200064-1.0-AWSVKuZT6T5DFUXvTHhyY6p1CQm3mZpQfFxyQYOSwoS5MC8hpZ0LowZMOHa6RZyrqaE+SElN6+1QpKXXk3JAtvw='
}


def date_now():
    # Get the current date and time
    current_datetime = datetime.now()
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
    
    pacific_timezone = pytz.timezone('America/Los_Angeles')
    
    # Get the current time in UTC
    current_time_utc = datetime.utcnow()
    
    # Convert current time to Pacific timezone
    current_time_pacific = current_time_utc.astimezone(pytz.utc).astimezone(pacific_timezone)
    
    # Add 5 minutes to the current time
    future_time_pacific = current_time_pacific + timedelta(minutes=5)
    
    # Set the date to "2024-02-27"
    future_time_pacific = future_time_pacific.replace(year=year, month=month, day=day)
    
    # Format the future time to RFC3339 format
    rfc3339_future_time = future_time_pacific.isoformat()
    
    return rfc3339_future_time


def naming_date():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the datetime object as a string with the desired format
    formatted_date = current_datetime.strftime('%Y%d%m-%H%M%S')
    return formatted_date


def get_campaigns() -> object:
    global campaigns
    url = "https://api.brevo.com/v3/emailCampaigns?excludeHtmlContent=true"
    payload = json.dumps({})
    campaigns = make_request("GET", payload, url)['campaigns']
    matching_campaigns = [campaign for campaign in campaigns if 'E3' in campaign['name']]
    matching_campaigns = sorted(matching_campaigns, key=lambda x: x['name'], reverse=True)
    campaign_data = list()
    for c in matching_campaigns:
        campaign_data.append({"campaign_list_id": c['recipients']['lists'][0], "campaign_name": c['name'], "campaign_id": c['id']})

    return campaign_data


    #campaign_lists = [__list['recipients'] for __list in matching_campaigns]
    #campaign_list = [__list['lists'] for __list in campaign_lists]
    #campaign_list = campaign_list[0][0]
    #return {"campaign_list_id": campaign_list, "campaign_name": campaign_name, "campaign_id": matching_campaigns[0]['id']}


def contact_list(campaign_info: object) -> object:
    try:
        url = f"https://api.brevo.com/v3/contacts/lists/{campaign_info['campaign_list_id']}/contacts"
        return make_request("GET", json.dumps({"listId": campaign_info['campaign_list_id']}), url)['contacts']
    except Exception as e:
        print(str(e))


def email_to_url_encoded(email):
    encoded_email = urllib.parse.quote(email)
    return encoded_email


def get_bounce_backs(email: object):
    url = f"https://api.brevo.com/v3/contacts/{email_to_url_encoded(email)}/campaignStats"
    return make_request("GET", {}, url)


def chunk_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


def remove_from_contact_list(emails: list, campaign: object):
    url = f"https://api.brevo.com/v3/contacts/lists/{campaign['campaign_list_id']}/contacts/remove"
    data = json.dumps({"REMOVECONTACTFROMLISTBYEMAILS": True, "emails": emails})
    for chunk in chunk_list(emails, 150):
        print(chunk)
        make_request("POST", data, url)


def write_email_bounces(file_path, input_list):
    with open(file_path, 'w') as file:
        if input_list:
            for item in input_list:
                file.write(str(item) + '\n')
        else:
                file.write("No Bounced Emails Today")


def get_bounced_or_rejected(c):
    try:
        for item in contact_list(c):
            #print(item['email'] + " : " + json.dumps(item['attributes']))
            msg_data = get_bounce_backs(item['email'])
            if 'hardBounces' in msg_data.keys():
                bounce_emails.append(item['email'])
            if 'softBounces' in msg_data.keys():
                bounce_emails.append(item['email'])
    except Exception as e:
        print(str(e))



def main():
    global bounce_emails
    campaigns = get_campaigns()
    bounce_emails=list()
    for c in campaigns:
        get_bounced_or_rejected(c)
        #remove_from_contact_list(emails=bounce_emails, campaign=c)
        file_path = f"{app_files}/users/{user_id}/bounce_lists/{c['campaign_name']}_bounce_list.csv"
        if os.path.exists(file_path):
            print(f"Bounce list already exists: {file_path}")
        else:
            write_email_bounces(file_path, bounce_emails)


if __name__ == "__main__":
    main()
    #print(get_campaigns())


