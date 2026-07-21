import os
import time
import requests
import smtplib
import schedule
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from notion_client import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

USE_DISCORD = os.getenv("USE_DISCORD", "false").lower() == "true"
USE_EMAIL = os.getenv("USE_EMAIL", "false").lower() == "true"

# Tier to Days mapping
TIER_MAP = {
    "Inner Circle": 30,
    "Mentor": 90,
    "Colleague": 90,
    "Acquaintance": 180,
    "Alumni": 180
}

# Initialize Notion Client
notion = Client(auth=NOTION_TOKEN)

def send_discord_notification(payload):
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("[ERROR] Discord Webhook URL is missing.")
        return
    
    data = {"content": payload}
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print("[SUCCESS] Sent Discord notification.")
    else:
        print(f"[ERROR] Failed to send Discord notification: {response.text}")

def send_email_notification(payload):
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")
    recipient = os.getenv("EMAIL_RECIPIENT")
    
    if not all([smtp_server, smtp_username, smtp_password, recipient]):
        print("[ERROR] Email configuration is incomplete.")
        return

    msg = MIMEMultipart()
    msg['From'] = smtp_username
    msg['To'] = recipient
    msg['Subject'] = "Personal CRM: Action Required"
    
    # Format payload for email reading
    body = payload.replace("**", "")
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)
        server.quit()
        print("[SUCCESS] Sent Email notification.")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def process_notion_db():
    print(f"[{datetime.now()}] Waking up CRM Engine...")
    
    try:
        # Fetch all contacts from Notion Database
        results = notion.databases.query(
            database_id=NOTION_DATABASE_ID
        ).get("results")
    except Exception as e:
        print(f"[ERROR] Failed to fetch Notion DB: {e}")
        return

    overdue_contacts = []

    for page in results:
        page_id = page["id"]
        props = page["properties"]
        
        # Extract properties
        try:
            name = props["Name"]["title"][0]["text"]["content"]
            tier = props["Tier"]["select"]["name"]
            last_contacted_str = props["Last_Contacted_Date"]["date"]["start"]
            rich_text_notes_arr = props["Rich_Text_Notes"]["rich_text"]
            notes = rich_text_notes_arr[0]["text"]["content"] if rich_text_notes_arr else "No notes."
            contacted_today = props["I_Contacted_Them_Today"]["checkbox"]
        except Exception as e:
            # Skip rows that are improperly formatted or missing data
            continue
        
        # 1. Check Reset Trigger
        if contacted_today:
            print(f"[*] Resetting timer for {name}...")
            today_str = datetime.now().strftime("%Y-%m-%d")
            
            # Patch the Notion DB to reset date and uncheck box
            notion.pages.update(
                page_id=page_id,
                properties={
                    "Last_Contacted_Date": {"date": {"start": today_str}},
                    "I_Contacted_Them_Today": {"checkbox": False}
                }
            )
            # Timer is reset, move to next contact
            continue
            
        # 2. Calculate Interval Math
        if not last_contacted_str or tier not in TIER_MAP:
            continue
            
        last_contacted_date = datetime.strptime(last_contacted_str, "%Y-%m-%d")
        delta = (datetime.now() - last_contacted_date).days
        allowed_interval = TIER_MAP[tier]
        
        if delta > allowed_interval:
            overdue_contacts.append(
                f"**{name}**\n- Days Overdue: {delta - allowed_interval} (Last contacted {delta} days ago)\n- Notes: {notes}\n"
            )
            
    # 3. Fire Notifications
    if overdue_contacts:
        print(f"[*] Found {len(overdue_contacts)} overdue contacts.")
        
        payload_header = "🚨 **Personal CRM Action Required** 🚨\nThe following contacts have breached their intervals:\n\n"
        payload_body = "\n".join(overdue_contacts)
        full_payload = payload_header + payload_body
        
        if USE_DISCORD:
            send_discord_notification(full_payload)
        
        if USE_EMAIL:
            send_email_notification(full_payload)
            
    else:
        print("[*] All relationships are warm. No action required today.")

    print(f"[{datetime.now()}] CRM Engine returning to sleep.")

if __name__ == "__main__":
    print("========================================")
    print("Personal Networking CRM Engine Started")
    print("Scheduler armed for 03:30 AM daily.")
    print("========================================")
    
    # Run once on startup to verify it works
    process_notion_db()
    
    # Schedule the daily job
    schedule.every().day.at("03:30").do(process_notion_db)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
