import time
import schedule
from datetime import datetime
from src.config import Config
from src.notion_service import NotionService

def run_job():
    print("========================================")
    service = NotionService()
    service.process_database()
    print(f"[{datetime.now()}] CRM Engine returning to sleep.")
    print("========================================")

if __name__ == "__main__":
    print("========================================")
    print("Starting Personal Networking CRM")
    
    try:
        Config.validate()
        print("[SUCCESS] Environment configured correctly.")
    except ValueError as e:
        print(f"[FATAL ERROR] {e}")
        exit(1)
        
    print("Scheduler armed for 03:30 AM daily.")
    print("========================================")
    
    # Run once immediately to verify mechanics
    run_job()
    
    # Arm the daily trigger
    schedule.every().day.at("03:30").do(run_job)
    
    while True:
        schedule.run_pending()
        time.sleep(60)
