#!/usr/bin/env python3.11
import shutil
from openai import OpenAI
import os
from datetime import datetime,timezone
import json
from integrations.brevo.BrevoSend  import build_campaign, return_campaign_files, delete_campaign_files
from integrations.brevo.BrevoWorkflow import adhoc_build_campaign
# from .BrevoUpdateContactList import main as update_contact_list
from integrations.brevo.BrevoBounceList import main as gen_bounce_list
from integrations.google.gmail import download_csv
import string
import random
from config import config


OpenAI.api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI()
fqdn = os.getenv('HOST')
port = os.getenv('PORT')
current_directory = os.path.dirname(os.path.abspath(__file__))
app_files = os.getenv('APP_FILES')

# def copy_contacts(file_name):
#     shutil.copy(f"{app_files}/users/{user_id}/user_contacts.csv", file_name)


def current_date():
    # Get the current date and time in UTC
    current_gmt_datetime = datetime.now(timezone.utc)
    # Format the date as YYYY-MM-DD
    formatted_date_gmt = current_gmt_datetime.strftime('%Y-%m-%d')
    return formatted_date_gmt


def chatgpt_parse_date(phrase):
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract and clarify the date and convirt the date to the format YYYYMMDD from this phrase return only the converted date in relation to today, the current date {current_date()}. Also only return the numbers of the formatted date and nothing else all of the time. Provide no explanation: '{phrase}'"}
      ]
    )

    return response.choices[0].message.content.strip()


def create_email(phrase):
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Create the text for a sample email with the following requirements and do not include the subject: '{phrase}'"}
      ]
    )

    return response.choices[0].message.content.strip()


def chatgpt_parse_filename(message):
    OpenAI.api_key = os.getenv('OPENAI_API_KEY')
    client = OpenAI()
    # Send the phrase to ChatGPT to get a more straightforward date expression
    response = completion = client.chat.completions.create(
      #model="gpt-3.5-turbo",
      model="gpt-4",
      messages=[
          {"role": "system", "content": "You are a helpful assistant that does only what I ask and exactly as I ask."},
          {"role": "user", "content": f"Extract the text here that represents a file name and convert to a purely a string and only the file name as a string. Do not return as markup."}
      ]
    )

    return response.choices[0].message.content.strip()


class Functions:

    user_id = None  # Class attribute

    @classmethod
    def set_user_id(cls, user_id):
        """Set the user_id for the class."""
        cls.user_id = user_id
        print(f"Setting user ID!! {cls.user_id}")
    
    @classmethod
    def get_user_id(cls):
        """Get the user_id from the class."""
        return cls.user_id

    @staticmethod
    def display_user_id():
        """Static method to display the user_id."""
        print(f"The user_id is: {Functions.user_id}")

    def list_campaigns():
        campaign_files = return_campaign_files()
        if campaign_files:
            return '\n- '.join([''] + campaign_files)
        else:
            return "No campaigns currently scheduled."
    
    list_campaigns_JSON = {
        "name": "list_campaigns",
        "description": "list campaigns",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }

    def get_random_digit():
        return random.randint(0,9)
    
    get_random_digit_JSON = {
        "name": "get_random_digit",
        "description": "Get a random digit",
        "parameters": {
            "type": "object",
            "properties": {},
        }
    }

    def get_random_letters(count: int, case_sensitive: bool = False):
        return ''.join(random.choices(string.ascii_letters if case_sensitive else string.ascii_uppercase, k=count))

    get_random_letters_JSON = {
        "name": "get_random_letters",
        "description": "Get a string of random letters",
        "parameters": {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": "Number of letters to return"},
                "case_sensitive": {"type": "boolean", "description": "Whether to include lower-case letters.  Default only returns upper-case letters."}
            },
            "required": ["count"]
        }
    }

    def get_sample_email_text( email_requirements: str):
        #return "sample email text response"
        return create_email(email_requirements)
    
    get_sample_email_text_JSON = {
        "name": "get_sample_email_text",
        "description": "Create the text for sample email. Don't include the subject.",
        "parameters": {
            "type": "object",
            "properties": {
                "email_requirements": {"type": "string", "description": "The requirements for the email that the user describes."},
                
                },
        }
    }

    def get_email_editor():
        return f"Use the email editor at [Editor](http://{fqdn}:{port}/email_edit)"
    
    get_email_editor_JSON = {
        "name": "get_email_editor",
        "description": "Return the link the the email editor to the user.",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }

    def get_contact_csv():
        return "Download contacts CSV doc here: [Contact Spreadsheet](http://docs.google.com/spreadsheets/d/1rwtospaUv6FBfYn9YYXNktJWUGxhGHJyqY_zWB9RWmY/edit?usp=sharing)"
    
    get_contact_csv_JSON = {
        "name": "get_contact_csv",
        "description": "Return the link for the contact csv. Get contacts.",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }

    def get_reports():
        return f"View the report at [Report](http://{fqdn}:{port}/reports)"
    
    get_reports_JSON = {
        "name": "get_reports",
        "description": "Get the latest reports, get the latest report link,  or generate report and present ink to the user.",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }

    def get_archived_reports():
        return f"View archived reports at [Reports](http://{fqdn}:{port}/reports)"
    
    get_archived_reports_JSON = {
        "name": "get_archived_reports",
        "description": "Get archived reports, get the archived report link.",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }

    def get_bounce_lists():
        return f"View archived bounce lists at [Bounce List/Rejected](http://{fqdn}:{port}/bounce_lists)"
    
    get_bounce_lists_JSON = {
        "name": "get_bounce_lists",
        "description": "Get bounce lists, get the bounce lists link, get reject lists,",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }


    def get_contact_lists():
        return f"View archived contact lists at [Contacts](http://{fqdn}:{port}/contacts)"
    
    get_contact_lists_JSON = {
        "name": "get_contact_lists",
        "description": "Get archived contacts lists, get the archived contacts.",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }

    def get_email_designs():
        return f"View archived email designs at [Email Designs](http://{fqdn}:{port}/email_designs)"
    
    get_email_designs_JSON = {
        "name": "get_email_designs",
        "description": "Get email designs, get the email designs link.",
        "parameters": {
            "type": "object",
            "properties": {
                
            },
        }
    }


    def show_help():
        __help = '''
- Create a campaign with the subject 'Sample campaign' and send it on 5/19/2024
- Show scheduled campaigns
- Create a sample email about teachers attending a training event, make it heartfelt and inspiring
- Delete campaign(s) 'A copy and pasted campaign name list of campaign names'
- Show reports
- Show contacts
- Show email editor
- Show reports
- Show bounce lists
- Show email designs
- Show contact lists
- Help

'''
        return __help
    
    show_help_JSON = {
        "name": "show_help",
        "description": "Show help",
            "properties": {
                
            },
    }


    # def update_contacts(message):
    #     return update_contact_list()
    
    # update_contacts_JSON = {
    #     "name": "update_contacts",
    #     "description": "when the user request to Update contacts. Add contacts. Upload contacts.",
    #     "parameters": {
    #         "type": "object",
    #         "properties": {
    #             "message": {"type": "string", "description": "Update contacts. Add contacts. Upload contacts."},
    #         },
    #     }
    # }


    def delete_campaigns( campaigns: object):
        return delete_campaign_files( campaigns)
        #return "OK"
    
    delete_campaigns_JSON = {
        "name": "delete_campaigns",
        "description": "Delete campaigns",
        "parameters": {
            "type": "object",
            "properties": {
                "campaigns": {"type": "string", "description": "A list of campaign names provided by the user. Get the campaign names from the users message then provide them as a json list to the function."},
                
            },
            "required": ["campaigns"]
        }
    }


    #def copy_contacts(file_name):
    #    shutil.copy("/var/www/html/uploads/user_contacts.csv", file_name)

    
    def schedule_email_campaign(subject, sender_name, scheduledAt, emails=None, test="yes"):
        #if emails:
        #    brevo_load_contacts(adhoc_contacts=emails)
        schedule_date = chatgpt_parse_date(scheduledAt)
        download_csv(user_id=Functions.user_id, path=f'{app_files}/users/{Functions.user_id}/contacts/{schedule_date}-E3-Campaign.csv')
        if (subject and scheduledAt):
            data = {
                    "subject": subject,
                    "sender_name": sender_name,
                    "scheduledAt": schedule_date,
                    "emails" : emails,
                    "test": test,
                    }
            #if build_campaign(data):
            
            # Copy user uploaded contacts to the correct location
            # copy_contacts(f'{app_files}/users/{user_id}/contacts/{schedule_date}-E3-Campaign.csv')
            if os.path.exists(f'{app_files}/users/{Functions.user_id}/contacts/{schedule_date}-E3-Campaign.csv'):
                print("File exists, continuing...")
                adhoc_build_campaign(Functions.user_id, data)
                return "Campaign scheduled"
            else:
                return "Error: You did not upload your contacts"

    schedule_email_campaign_JSON = {
        "name": "schedule_email_campaign",
        "description": "Send or schedule campaign",
        "parameters": {
            "type": "object",
            "properties": {
                "emails": {"type": "string", "description": "A list of emails that the user would like to use to send the email to. This gets added to the standard email list."},
                "subject": {"type": "string", "description": "The subject that the user would like to use in the email."},
                "scheduledAt": {"type": "string", "description": f"Campaign scheduling time."},
                "sender_name": {"type": "string", "description": "The name of the email campaign sender."},
                "test": {"type": "string", "description": "Determine whether this campaign schedule is test or not. By default if not set make this set to yes. If the user want to run a real campaign set to no."},
                
            },
            "required": ["subject", "sender_name", "scheduledAt"]
        }
    }


if __name__ == '__main__':
    print(chatgpt_parse_date("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign today"))
    print(chatgpt_parse_date("schedule a campaign with the subject test subject, the sender name miguel, schedule the campaign this friday"))
