import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Central configuration class that parses and validates environment variables."""
    
    NOTION_TOKEN = os.getenv("NOTION_TOKEN")
    NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")
    
    USE_DISCORD = os.getenv("USE_DISCORD", "false").lower() == "true"
    USE_EMAIL = os.getenv("USE_EMAIL", "false").lower() == "true"
    
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
    
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
    EMAIL_RECIPIENT = os.getenv("EMAIL_RECIPIENT")

    @classmethod
    def validate(cls):
        """Validates that all required configuration variables are present."""
        if not cls.NOTION_TOKEN:
            raise ValueError("NOTION_TOKEN is missing from environment.")
        if not cls.NOTION_DATABASE_ID:
            raise ValueError("NOTION_DATABASE_ID is missing from environment.")
            
        if cls.USE_DISCORD and not cls.DISCORD_WEBHOOK_URL:
            raise ValueError("USE_DISCORD is true, but DISCORD_WEBHOOK_URL is missing.")
            
        if cls.USE_EMAIL and not all([cls.SMTP_SERVER, cls.SMTP_USERNAME, cls.SMTP_PASSWORD, cls.EMAIL_RECIPIENT]):
            raise ValueError("USE_EMAIL is true, but SMTP credentials are incomplete.")
