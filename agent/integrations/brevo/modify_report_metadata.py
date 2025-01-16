import json
import os

reply_to_email = os.getenv('REPLY_TO_EMAIL')
html_report_url = os.getenv('HTML_REPORT_URL')
sender_email = os.getenv('SENDER_EMAIL')

def modify_report_metadata():


    current_directory = os.path.dirname(os.path.abspath(__file__))

    # Specify the filename
    filename = f'{current_directory}/notify.json'

    # Load the JSON data from the file
    with open(filename, 'r') as file:
        data = json.load(file)

    # Modify specific keys
    data['replyTo'] = reply_to_email
    data['htmlUrl'] = html_report_url
    data['sender']['email'] = sender_email

    # Write the modified data back to the same file
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

    print("File notify.json updated successfully.")
