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
fqdn = os.getenv('HOST')
port = os.getenv('REPORT_ACCESS_PORT')


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


def get_campaign_schedule_file_data(file_name):
    campaign_data = dict()
    with open(file_name, "r") as file:
        campaign_data = json.load(file)
    # URL point to a route in /routes -> /notify_report
    campaign_data['htmlUrl'] = f"http://{fqdn}:{port}/notify_report"
    return campaign_data


def send_report_email(user_id) -> object:
    print("Sending Campaign...")
    url = "https://api.brevo.com/v3/emailCampaigns"
    payload = get_campaign_schedule_file_data(f'{current_directory}/notify.json')
    payload['scheduledAt'] = date_now()
    payload = json.dumps(payload, indent=4)
    resp = make_request("POST", payload, url)
    print(f"Notification sent successfully.")
    return resp


if __name__ == "__main__":
    print(send_campaign())



