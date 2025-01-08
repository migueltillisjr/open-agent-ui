#!/usr/bin/env python3.11
import json
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from jinja2 import Environment, FileSystemLoader
from BrevoSend import recent_campaign_reports
from latest.assistant.integrations.brevo.MakeRequest import make_request
from BrevoBounceList import main as bounce_backs
import time

# Data for the report
campaigns = [{    "id": 24,    "name": "20242402-035525-E3-Campaign",    "type": "classic",    "status": "sent",    "testSent": False,    "header": "If you are not able to see this mail, click {here}",    "footer": "If you wish to unsubscribe from our newsletter, click {here}",    "sender": {        "name": "noreply",        "id": 3,        "email": "noreply@ldm-group.org"    },    "replyTo": "noreply@ldm-group.org",    "toField": "{{contact.FIRSTNAME}} {{contact.LASTNAME}}",    "previewText": "",    "tag": "E3-Campaign",
    "inlineImageActivation": False,
    "mirrorActive": False,
    "recipients": {
        "lists": [9],
        "exclusionLists": []
    },
    "statistics": {
        "globalStats": {
            "uniqueClicks": 0,
            "clickers": 0,
            "complaints": 0,
            "delivered": 0,
            "sent": 0,
            "softBounces": 0,
            "hardBounces": 0,
            "uniqueViews": 0,
            "unsubscriptions": 0,
            "viewed": 0,
            "trackableViews": 0,
            "trackableViewsRate": 0,
            "estimatedViews": 0
        },
        "campaignStats": [
            {
                "listId": 9,
                "uniqueClicks": 0,
                "clickers": 0,
                "complaints": 0,
                "delivered": 3,
                "sent": 10,
                "softBounces": 2,
                "hardBounces": 5,
                "uniqueViews": 0,
                "trackableViews": 0,
                "unsubscriptions": 0,
                "viewed": 0,
                "deferred": 0
            }
        ],
        "mirrorClick": 0,
        "remaining": 0,
        "linksStats": {},
        "statsByDomain": {},
        "statsByDevice": {
            "desktop": {
                "mac": {
                    "clickers": 0,
                    "uniqueClicks": 0,
                    "viewed": 0,
                    "uniqueViews": 0,
                    "trackableViews": 0
                },
                "windows": {
                    "clickers": 0,
                    "uniqueClicks": 0,
                    "viewed": 0,
                    "uniqueViews": 0,
                    "trackableViews": 0
                },
                "otherSystem": {
                    "clickers": 0,
                    "uniqueClicks": 0,
                    "viewed": 0,
                    "uniqueViews": 0,
                    "trackableViews": 0
                }
            },
            "mobile": {
                "androidMobile": {
                    "clickers": 0,
                    "uniqueClicks": 0,
                    "viewed": 0,
                    "uniqueViews": 0,
                    "trackableViews": 0
                },
                "iPhone": {
                    "clickers": 0,
                    "uniqueClicks": 0,
                    "viewed": 0,
                    "uniqueViews": 0,
                    "trackableViews": 0
                }
            },
            "tablet": {
                "androidTablet": {
                    "clickers": 0,
                    "uniqueClicks": 0,
                    "viewed": 0,
                    "uniqueViews": 0,
                    "trackableViews": 0
                },
                "appleIPad": {
                    "clickers": 0,
                    "uniqueClicks": 0,
                    "viewed": 0,
                    "uniqueViews": 0,
                    "trackableViews": 0
                }
            }
        },
        "statsByBrowser": {
            "android": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "chrome": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "edge": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "firefox": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "internetExplorer": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "opera": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "safari": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "electron": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "mailChannelsScanner": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "microsoft": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "mozilla": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "outlookExpress": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "thunderbird": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "yahooMailProxy": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            },
            "unknown": {
                "clickers": 0,
                "uniqueClicks": 0,
                "viewed": 0,
                "uniqueViews": 0,
                "trackableViews": 0
            }
        }
    },
    "subject": "My {{params.subject}}",
    "scheduledAt": "2024-02-23T16:56:26.000-10:00",
    "createdAt": "2024-02-23T17:55:27.000-10:00",
    "modifiedAt": "2024-02-23T17:55:27.000-10:00",
    "shareLink": "http://sh1.sendinblue.com/ndz6if53sc.html",
    "sentDate": "2024-02-23T17:56:39.000-10:00",
    "sendAtBestTime": False,
    "abTesting": False
}]


# Function to generate a base64 encoded image for embedding in HTML
def plot_stats(stats, title):
    labels = ['Delivered', 'Sent', 'Soft Bounces', 'Hard Bounces', 'Unsubscriptions', 'Clickers', 'Viewed', 'Complaints']
    if not stats['campaignStats']:
        return False
    elif stats['campaignStats']:
        values = [
            stats['campaignStats'][0]['delivered'],
            stats['campaignStats'][0]['sent'],
            stats['campaignStats'][0]['softBounces'],
            stats['campaignStats'][0]['hardBounces'],
            stats['campaignStats'][0]['unsubscriptions'],
            stats['campaignStats'][0]['clickers'],
            stats['campaignStats'][0]['viewed'],
            stats['campaignStats'][0]['complaints']
        ]

        # Filter out categories with zero data for the first pie chart (Delivered)
        filtered_labels_delivered = []
        filtered_values_delivered = []
        for label, value in zip(labels, values):
            if label == 'Delivered':
                filtered_labels_delivered.append(label)
                filtered_values_delivered.append(value)

        if not filtered_values_delivered:
            return False

        # Filter out 'Delivered' category for the second pie chart
        filtered_labels_other = []
        filtered_values_other = []
        for label, value in zip(labels, values):
            if label != 'Delivered' and value > 0:
                filtered_labels_other.append(label)
                filtered_values_other.append(value)

        # Create the plots
        fig, axs = plt.subplots(1, 3, figsize=(18, 6))

        # Pie chart for 'Delivered'
        axs[0].pie(filtered_values_delivered, labels=filtered_labels_delivered, autopct='%1.1f%%', startangle=140)
        axs[0].set_title('Delivered')

        # Pie chart for other categories
        axs[1].pie(filtered_values_other, labels=filtered_labels_other, autopct='%1.1f%%', startangle=140)
        axs[1].set_title('Other Categories')

        # Bar chart
        axs[2].bar(labels, values, color='skyblue')
        axs[2].set_title('Bar Chart')
        axs[2].set_xticks(labels)
        axs[2].tick_params(axis='x', rotation=45)

        fig.suptitle(title)
        plt.tight_layout()

        # Convert the plot to base64 encoded image
        img = BytesIO()
        plt.savefig(img, format='png')
        plt.close()
        img.seek(0)

        return base64.b64encode(img.getvalue()).decode('utf-8')


def write_recipiants(campaign_id):
    url = f"https://api.brevo.com/v3/emailCampaigns/{campaign_id}/exportRecipients"
    data = json.dumps({"recipientsType": "all"})
    make_request("POST", data, url)


def get_campaign(campaign_id: int) -> object:
    time.sleep(2)
    global campaigns
    url = f"https://api.brevo.com/v3/emailCampaigns/{campaign_id}?excludeHtmlContent=true"
    payload = json.dumps({})
    campaign_data = make_request("GET", payload, url)
    return campaign_data


def contact_list(list_id) -> object:
    url = f"https://api.brevo.com/v3/contacts/lists/{list_id}/contacts"
    return make_request("GET", json.dumps({}), url)


def write_contact_lists(campaign_name, recipients):
    with open(f"/var/www/html/uploads/email_lists/{campaign_name}.csv", "w") as file:
        if 'contacts' in recipients:
            for r in recipients['contacts']:
                file.write(f"{r['email']}\n")
        file.write("\n")


def initiate():
    campaigns = recent_campaign_reports()
    # Generate charts for each campaign
    bounce_backs()
    for campaign in campaigns:
        # copy campaign to new location
        c = get_campaign(campaign['id'])['recipients']['lists'][0]
        campaign['recipients'] = contact_list(c)
        campaign['bounce_backs'] = campaign['name'] + '_bounce_backs.csv'
        write_contact_lists(campaign['name'], campaign['recipients'])
        
        chart = plot_stats(campaign['report']['statistics'], f"Statistics for {campaign['name']}")
        #chart = plot_stats(campaign['report']['statistics'], f"Statistics for {campaign['name']}")
        campaign['chart'] = chart

    # Setup Jinja2 environment
    env = Environment(loader=FileSystemLoader('/var/www/html/uploads'))
    template = env.get_template('report_template.html')

    # Render the template with data
    html_content = template.render(campaigns=campaigns)

    # Write the HTML content to a file
    with open('/var/www/html/uploads/campaign_report.html', 'w') as file:
        file.write(html_content)


if __name__ == "__main__":
    initiate()


