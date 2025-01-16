import schedule
import threading
import time
from ..integrations.brevo.SendReport import send_report_email
from ..integrations.brevo.adhoc_gen_report import initiate as generate_report
from ..integrations.brevo.BrevoSend import schedule_campaign
from ..config import db
from ..models import User  # Assuming User is your model
import os

scheduler_running = False

def create_directory_structure(base_path):
    # Define the directory structure
    structure = {
        "bounce_lists": [

        ],
        "campaigns": [

        ],
        "contacts": [

        ],
        "email_designs": [

        ],
        "email_lists": [

        ],
        "reports": [

        ],
        "templates": [
            "notify.html"
        ],
        "uploads": [
            "contacts.csv",
            "email_template.html",
            "email_templates",
            "latest.html",
            "user_contacts.csv"
        ],
        "": [  # Root-level files
            "campaign_report.html",
            "download.html",
            "email-design.html",
            "last_page_requested",
            "notify_template.html",
            "report_template.html",
            "user_contacts.csv"
        ]
    }

    # Create the structure
    for folder, files in structure.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        for file in files:
            file_path = os.path.join(folder_path, file)
            if "." in file:  # Create file if it has an extension
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "w") as f:
                    pass  # Create empty file

# # Define the base directory (user ID 1 as an example)
# base_dir = ""
# create_directory_structure(base_dir)


def process_user_jobs(user_id):
    """Process jobs for a specific user."""
    generate_report(user_id)
    send_report_email(user_id)
    schedule_campaign(user_id)

def schedule_job():
    """Schedule jobs for all users."""
    users = User.query.with_entities(User.id).all()  # Retrieve all user IDs from the database
    for user in users:
        user_id = user.id
        process_user_jobs(user_id)

# Function to run the scheduled jobs continuously in a background thread
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)  # Check every second

def start_scheduler():
    """Start the scheduler in a background thread."""
    global scheduler_running
    if not scheduler_running:
        # Schedule the jobs
        schedule.every().day.at("10:30").do(schedule_job)  # Run job every day at 10:30 AM
        # Uncomment below line to run the job every 5 minutes (for testing purposes)
        # schedule.every(5).minutes.do(schedule_job)

        # Start the scheduler thread
        scheduler_thread = threading.Thread(target=run_scheduler)
        scheduler_thread.daemon = True
        scheduler_thread.start()

        scheduler_running = True
        print({"message": "Scheduler started successfully!"})
    else:
        print({"message": "Scheduler is already running!"})
