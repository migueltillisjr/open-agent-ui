#!/usr/bin/env python3.11
import csv
import os
import inspect
import sys
import requests
import json
import time
import uuid
# from ApolloIO import load_contacts

global headers
global folder_id
global contact_list_name
global contact_list_id
global folder_name
global contacts
global campaign_name

current_directory = os.path.dirname(os.path.abspath(__file__))

config = object()
with open(f'{current_directory}/config.json', 'r') as file:
    config = json.load(file)
folder_name=config['folder_name']
contact_list_name=config['contact_list_name']
campaign_name=config['campaign_name']
fqdn = os.getenv('HOST')
port = os.getenv('PORT')
app_files = os.getenv('APP_FILES')


API_KEY='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'
headers = {
  'Accept': 'application/json',
  'Content-Type': 'application/json',
  'api-key': API_KEY,
  'Cookie': '__cf_bm=m0D5f_XED4_fm_jlOIpAAi6abzAK2gJhwuDm7yObxfE-1708200064-1.0-AWSVKuZT6T5DFUXvTHhyY6p1CQm3mZpQfFxyQYOSwoS5MC8hpZ0LowZMOHa6RZyrqaE+SElN6+1QpKXXk3JAtvw='
}


def current_function_name():
    # Get the frame of the caller
    caller_frame = inspect.currentframe().f_back.f_back
    # Get information about the calling function
    calling_function = inspect.getframeinfo(caller_frame).function
    return calling_function


def make_request(method: str, payload: object, url: str) -> object:
    try:
        response = requests.request(method, url, headers=headers, data=payload)
        if response.status_code > 299:
            error_message = f"HTTP Error {response.status_code}: {response.reason} | Response: {response.text}"
            raise Exception(error_message)
        response = json.loads(response.text)
        print(response)
        print(payload)
        return response
    except Exception as e:
        print("ERROR: " + current_function_name() + " | " + str(e))
        print(current_function_name())
        pass
        #sys.exit(1)


def folder_list() -> object:
    url = "https://api.brevo.com/v3/contacts/folders"
    return make_request("GET", {}, url)["folders"]


def folder_exists(response):
    global folder_id
    exists = False
    for item in response:
        if folder_name == item["name"]:
            folder_id = item["id"]
            print(f"Folder ID is {folder_id}")
            exists = True
            break
    return exists


def create_folder() -> object:
    url = "https://api.brevo.com/v3/contacts/folders"
    payload = json.dumps({
      "name": folder_name
    })
    resp = make_request("POST", payload, url)["folders"][0]
    folder_id=resp["id"]
    return resp


def contact_lists() -> object:
    url = "https://api.brevo.com/v3/contacts/lists"
    return make_request("GET", {}, url)["lists"]


def contact_list_exists(contact_lists) -> object:
    global contact_list_id
    exists = False
    for item in contact_lists:
        if contact_list_name == item["name"]:
            contact_list_id = item["id"]
            print(f"Contact list id is {contact_list_id}")
            exists = True
    return exists


def create_contact_list(list_name):
    global contact_list_id
    print("Create contact list")
    url = "https://api.brevo.com/v3/contacts/lists"
    payload = json.dumps({
      "folderId": folder_id,
      #"name": contact_list_name
      "name": list_name
    })
    
    resp = make_request("POST", payload, url)
    if 'lists' in resp.keys():
        contact_list_id = resp["lists"][0]["id"]
    else:
        contact_list_id = resp["id"]
    return resp


def split_list(lst, group_size):
    # Split list of emails because of request limitation of 150 email per import for Brevo API
    return [lst[i:i+group_size] for i in range(0, len(lst), group_size)]


def add_contacts_to_list(email_list: list, param_list_id=None) -> object:
    print("Add contacts to list")
    url = "https://api.brevo.com/v3/contacts/import"
    time.sleep(2)
    payload = json.dumps({
      "jsonBody": email_list,
      "listIds": [
        #contact_list_id
        param_list_id or contact_list_id
      ],
      "emailBlacklist": False,
      "smsBlacklist": False,
      "updateExistingContacts": True,
      "emptyContactsAttributes": True
    }, indent=4)
    print(payload)
    resp = make_request("POST", payload, url)
    print("Add contacts to list END")
    return resp
        

def adhoc_brevo_load_contacts(user_id, adhoc_contacts=False, file_path=f'{app_files}/users', list_name=contact_list_name):
    file_path=f'{file_path}/{user_id}/user_contacts.csv'
    list_id = str()
    if not folder_exists(folder_list()):
        create_folder()
    list_id = create_contact_list(list_name)['id']

    # Load AdHoc contacts
    if adhoc_contacts:
        grouped_contacts = split_list(load_contacts(file_path), 150)
        for contact_group in grouped_contacts:
            add_contacts_to_list(contact_group, list_id)

    return list_id


def brevo_load_contacts(user_id, adhoc_contacts=False, file_path=f'{app_files}/users', list_name=contact_list_name):
    file_path=f'{file_path}/{user_id}/user_contacts.csv'
    list_id = str()
    if not folder_exists(folder_list()):
        create_folder()
    if not contact_list_exists(contact_lists()):
        list_id = create_contact_list(list_name)['id']

    # Load apolloIO contacts
    if not adhoc_contacts:
        # Add 1,000 contacts to brevo from Apollo.io which has an export limit of 100 a request
        # Brevo has an import limit of 150 at a time
        for _ in range(10):
            try:
                grouped_contacts = split_list(load_contacts(file_path), 150)
                for contact_group in grouped_contacts:
                    add_contacts_to_list(contact_group)
            except Exception() as e:
                print(e)
                sys.exit(1)

    # Load AdHoc contacts
    if adhoc_contacts:
        grouped_contacts = split_list(load_contacts(file_path), 150)
        for contact_group in grouped_contacts:
            add_contacts_to_list(contact_group, list_id)


def load_contacts(user_id, file_path=f'{app_files}/users'):
    file_path=f'{file_path}/{user_id}/user_contacts.csv'
    user_list = []
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            for row in csv_reader:
                # Check if the row has exactly 3 columns
                if len(row) == 3:
                    user_list.append({"name": row[0], "email": row[1]})#, "country": row[2]})
                else:
                    print(f"Error: Row {csv_reader.line_num} does not have 3 columns. name, email, & country")
                    # Optionally handle the error here
                    # You can choose to skip the row or take other actions
                    # For now, skipping the row
    return user_list


def main(user_id, file_path=f'{app_files}/users'):
    file_path=f'{file_path}/{user_id}/user_contacts.csv'
    user_list = list()
    # Read contacts list csv & update contacts
    #file_path = '/var/www/html/uploads/user_contacts.csv'
    
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            #next(csv_reader)  # Skip header if present
            for row in csv_reader:
                print(row)
                user_list.append({"email": row[0], "name": row[1]})
                #for item in row:
                #    user_list.append(item)
        print(user_list)
        brevo_load_contacts(user_list)
        return "User list uploaded."
    else:
        return "No user list provided."



if __name__ == "__main__":
    main()
    #brevo_load_contacts([{"email": "migueltillisjr@gmail.com", "name": "Miguel", "country": "US"}])
    #brevo_load_contacts()


