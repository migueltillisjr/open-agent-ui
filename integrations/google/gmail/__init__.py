import gspread
import csv
from ....config import app, login_manager, db, bcrypt, app_workdir
import os

from google.oauth2.service_account import Credentials

current_directory = os.path.dirname(os.path.abspath(__file__))

gauth = os.getenv('GOOGLE_AUTH')

def download_csv(user_id=None, tab="SendList", spreadsheet_id='1rwtospaUv6FBfYn9YYXNktJWUGxhGHJyqY_zWB9RWmY', path=None):
    # Define the scope and create credentials object
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
    creds = Credentials.from_service_account_file(gauth, scopes=SCOPES)
    csv_file_paths=[
        f'{app_workdir}/app-files/users/{user_id}/uploads/contacts.csv',
        path
    ]

    # Connect to the Google Sheets API using gspread
    client = gspread.authorize(creds)

    # Open the Google Sheet by its ID
    spreadsheet = client.open_by_key(spreadsheet_id)

    # Select the specific tab by its name
    worksheet = spreadsheet.worksheet(tab)  # Replace with the actual tab name

    # Get all data from the selected tab
    rows = worksheet.get_all_values()

    # Specify the path to save the CSV file

    # Write the data to a CSV file
    for csv_file_path in csv_file_paths:
        if csv_file_path:
            with open(csv_file_path, mode='w+', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(rows)

    print(f"Tab '{worksheet.title}' downloaded as '{csv_file_path}'")

