from datetime import datetime
from notion_client import Client
from src.config import Config
from src.notification_engine import NotificationEngine

# Tier to Days mapping
TIER_MAP = {
    "Inner Circle": 30,
    "Mentor": 90,
    "Colleague": 90,
    "Acquaintance": 180,
    "Alumni": 180
}

class NotionService:
    """Handles fetching and processing the Notion CRM database."""
    
    def __init__(self):
        self.notion = Client(auth=Config.NOTION_TOKEN)

    def calculate_delta(self, last_contacted_str: str, current_date: datetime) -> int:
        """Returns the number of days since last contact."""
        last_contacted_date = datetime.strptime(last_contacted_str, "%Y-%m-%d")
        return (current_date - last_contacted_date).days

    def reset_timer(self, page_id: str, name: str, current_date: datetime):
        """Patches the Notion database to reset the date to today and uncheck the box."""
        print(f"[*] Resetting timer for {name}...")
        today_str = current_date.strftime("%Y-%m-%d")
        
        self.notion.pages.update(
            page_id=page_id,
            properties={
                "Last_Contacted_Date": {"date": {"start": today_str}},
                "I_Contacted_Them_Today": {"checkbox": False}
            }
        )

    def process_database(self, current_date=None):
        """The core engine that parses the DB and checks for overdue interactions."""
        if current_date is None:
            current_date = datetime.now()
            
        print(f"[{current_date}] Fetching CRM Database...")
        
        try:
            results = self.notion.databases.query(
                database_id=Config.NOTION_DATABASE_ID
            ).get("results")
        except Exception as e:
            print(f"[ERROR] Failed to fetch Notion DB: {e}")
            return

        overdue_contacts = []

        for page in results:
            page_id = page["id"]
            props = page["properties"]
            
            try:
                name = props["Name"]["title"][0]["text"]["content"]
                tier = props["Tier"]["select"]["name"]
                last_contacted_str = props["Last_Contacted_Date"]["date"]["start"]
                rich_text_notes_arr = props["Rich_Text_Notes"]["rich_text"]
                notes = rich_text_notes_arr[0]["text"]["content"] if rich_text_notes_arr else "No notes."
                contacted_today = props["I_Contacted_Them_Today"]["checkbox"]
            except Exception:
                # Skip malformed rows
                continue
            
            # Reset Trigger Logic
            if contacted_today:
                self.reset_timer(page_id, name, current_date)
                continue
                
            # Interval Math Logic
            if not last_contacted_str or tier not in TIER_MAP:
                continue
                
            delta = self.calculate_delta(last_contacted_str, current_date)
            allowed_interval = TIER_MAP[tier]
            
            if delta > allowed_interval:
                overdue_contacts.append(
                    f"**{name}**\n- Days Overdue: {delta - allowed_interval} (Last contacted {delta} days ago)\n- Notes: {notes}\n"
                )
                
        # Payload Dispatching
        if overdue_contacts:
            print(f"[*] Found {len(overdue_contacts)} overdue contacts.")
            payload_header = "🚨 **Personal CRM Action Required** 🚨\nThe following contacts have breached their intervals:\n\n"
            full_payload = payload_header + "\n".join(overdue_contacts)
            NotificationEngine.dispatch_payload(full_payload)
        else:
            print("[*] All relationships are warm. No action required today.")
