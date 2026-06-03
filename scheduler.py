import schedule
import time
from main_automated import run_automation
from datetime import datetime

def job():
    print(f"\n[{datetime.now()}] Running scheduled job...")
    run_automation()

# Schedule uploads every 6 hours
schedule.every(6).hours.do(job)

print("🤖 Scheduler started! Press Ctrl+C to stop.")
print("📅 Next run:", schedule.next_run())

while True:
    schedule.run_pending()
    time.sleep(60)