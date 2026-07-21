import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.config import Config

class NotificationEngine:
    """Handles dispatching of the overdue payloads to the user."""

    @staticmethod
    def send_discord_notification(payload: str):
        if not Config.USE_DISCORD:
            return
            
        data = {"content": payload}
        response = requests.post(Config.DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            print("[SUCCESS] Sent Discord notification.")
        else:
            print(f"[ERROR] Failed to send Discord notification: {response.text}")

    @staticmethod
    def send_email_notification(payload: str):
        if not Config.USE_EMAIL:
            return

        msg = MIMEMultipart()
        msg['From'] = Config.SMTP_USERNAME
        msg['To'] = Config.EMAIL_RECIPIENT
        msg['Subject'] = "Personal CRM: Action Required"
        
        # Remove bold markdown formatting for plaintext email
        body = payload.replace("**", "")
        msg.attach(MIMEText(body, 'plain'))
        
        try:
            server = smtplib.SMTP(Config.SMTP_SERVER, Config.SMTP_PORT)
            server.starttls()
            server.login(Config.SMTP_USERNAME, Config.SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
            print("[SUCCESS] Sent Email notification.")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")

    @classmethod
    def dispatch_payload(cls, payload: str):
        """Routes the payload to all enabled notification engines."""
        cls.send_discord_notification(payload)
        cls.send_email_notification(payload)
