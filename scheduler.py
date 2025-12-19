# main.py
import schedule
import time
import subprocess
from validate import validate_jobs
from outreach import generate_messages
from gsheet_integration import save_to_sheets
import sys


def job_pipeline():
    # 1️⃣ Scraping
    try:
        print("Scraping jobs...")
        subprocess.run([sys.executable, "-m", "pytest", "-s", "scraper.py", "--headless"],check=True)
        print("✅ Scraping completed")
    except Exception as e:
        print("❌ Scraping failed")
        return

    # 2️⃣ Validation
    try:
        print("Validating jobs...")
        validate_jobs()
        print("✅ Validation completed")
    except Exception as e:
        print("❌ Validation failed")
        return

    # 3️⃣ Message generation
    try:
        print("Generating messages...")
        generate_messages()
        print("✅ Message generation completed")
    except Exception as e:
        print("❌ Message generation failed")
        return

    # 4️⃣ Google Sheets
    try:
        print("Saving to Google Sheet...")
        save_to_sheets()
        print("✅ Saved to Google Sheets")
    except Exception as e:
        print("❌ Google Sheets upload failed")
        return

    print(" Pipeline completed successfully")


# Schedule daily at 8 AM
schedule.every().day.at("08:00").do(job_pipeline)


print("Scheduler running...")
while True:
    schedule.run_pending()
    time.sleep(60)

# for cronjob setup 
# 0 8 * * * /home/username/case_study_1/venv/bin/python /home/username/case_study_1/scheduler.py >> /home/username/case_study_1/logs/scheduler.log 2>&1


