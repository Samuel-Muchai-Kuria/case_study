import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def save_to_sheets(csv_file="jobs_with_messages.csv", sheet_name="Executive Assistant Job Outreach  Automation"):
    #  Set up Google Sheets authentication
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("bulkread_google_sheets.json", scope)
    client = gspread.authorize(creds)

    #  Open your Google Sheet
    sheet = client.open(sheet_name).worksheet("Job Applications")  

    # Create or open sheet
    try:
        sheet = client.open(sheet_name).sheet1
        sheet.clear()
    except gspread.SpreadsheetNotFound:
        sheet = client.create(sheet_name).sheet1
    
    df = pd.read_csv(csv_file)
    sheet.update([df.columns.values.tolist()] + df.values.tolist())

if __name__ == "__main__":
    save_to_sheets()