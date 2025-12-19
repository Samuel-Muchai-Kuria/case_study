# Job Outreach Automation System

An automated pipeline that scrapes executive and administrative assistant job postings, validates them against specific criteria, generates personalized outreach messages using AI, and exports results to Google Sheets.

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [Automation Setup](#automation-setup)
- [Updating Search Parameters](#updating-search-parameters)
- [Customizing LLM Prompts](#customizing-llm-prompts)
- [Troubleshooting](#troubleshooting)

## Features

- **Automated Job Scraping**: Scrapes job listings from TimesJobs for Executive and Admin Assistant positions
- **Intelligent Validation**: Filters jobs based on remote work availability, English requirements, and job titles
- **AI-Powered Outreach**: Generates personalized messages using Google's Gemini AI
- **Google Sheets Integration**: Automatically exports results to Google Sheets
- **Scheduled Execution**: Runs daily at 8 AM using Python's schedule library

## Architecture

The system consists of five main components:

1. **scraper.py** - Web scraping using SeleniumBase
2. **validate.py** - Job validation and filtering
3. **outreach.py** - AI message generation using Gemini
4. **gsheet_integration.py** - Google Sheets export
5. **scheduler.py** - Pipeline orchestration and scheduling

## Installation

### Prerequisites

- Python 3.8 or higher
- Google Cloud service account with Sheets API access
- Gemini API key

### Step 1: Clone and Setup Virtual Environment

```bash
# Create project directory
mkdir job_automation
cd job_automation

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install seleniumbase pandas gspread oauth2client python-dotenv google-genai schedule
```

### Step 3: Setup Google Sheets Authentication

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API
4. Create a service account and download the JSON key file
5. Rename the key file to `bulkread_google_sheets.json` and place it in the project root
6. Share your target Google Sheet with the service account email

### Step 4: Setup Gemini API

1. Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a `.env` file in the project root:

```env
gemini_api_key=YOUR_GEMINI_API_KEY_HERE
```

### Step 5: Create Log Directory

```bash
mkdir logs
```

## Configuration

### Google Sheets Configuration

In `gsheet_integration.py`, update the sheet name if needed:

```python
def save_to_sheets(csv_file="jobs_with_messages.csv", 
                   sheet_name="Executive Assistant Job Outreach Automation"):
```

### Validation Rules

Edit `validate.py` to modify job filtering criteria:

```python
# Current validation checks for:
# - Remote work (in location or description)
# - English communication requirements
# - Specific job titles
```

## Running the Application

### Manual Execution

Run the entire pipeline once:

```bash
python scheduler.py
```

Or run individual components:

```bash
# Scraping only
pytest -s scraper.py --headless

# Validation only
python validate.py

# Message generation only
python outreach.py

# Google Sheets upload only
python gsheet_integration.py
```

### Testing the Scraper

```bash
# Run with visible browser (for debugging)
pytest -s scraper.py

# Run headless (production mode)
pytest -s scraper.py --headless
```

## Automation Setup

The system uses Python's `schedule` library to run daily at 8 AM.

### Method 1: Keep Python Script Running

Simply run the scheduler script and keep it running:

```bash
python scheduler.py
```

The script will continue running and execute the pipeline daily at 8:00 AM.

### Method 2: Using Cron (Linux/macOS)

For production environments, use cron for better reliability:

```bash
# Edit crontab
crontab -e

# Add this line (adjust paths to your setup)
0 8 * * * /home/username/job_automation/venv/bin/python /home/username/job_automation/scheduler.py >> /home/username/job_automation/logs/scheduler.log 2>&1
```

**Cron Schedule Explanation:**
- `0 8 * * *` - Run at 8:00 AM every day
- First path: Python interpreter in your virtual environment
- Second path: scheduler.py script location
- `>> logs/scheduler.log` - Append output to log file
- `2>&1` - Redirect errors to the same log file

### Method 3: Using Windows Task Scheduler

1. Open Task Scheduler
2. Create Basic Task
3. Set trigger to "Daily" at 8:00 AM
4. Action: Start a program
   - Program: `C:\path\to\job_automation\venv\Scripts\python.exe`
   - Arguments: `C:\path\to\job_automation\scheduler.py`
   - Start in: `C:\path\to\job_automation`

### Verifying Scheduled Execution

Check the log file to verify runs:

```bash
tail -f logs/scheduler.log
```

## Updating Search Parameters

### Changing Job Positions

Edit `scraper.py`:

```python
def test_scrape_positions(self):
    positions = ["Executive Assistants", "Admin Assistants", "Personal Assistants"]
    for pos in positions:
        self.scrape_jobs_for_position(pos)
```

### Modifying Page Limits

In `scraper.py`, adjust the maximum pages to scrape:

```python
total_pages = min(total_pages, 20)  # Change 20 to desired number
```

### Adjusting Job Validation Criteria

Edit `validate.py` to modify filtering rules:

```python
# Add or modify validation rules
if "remote" in location or "remote" in desc:
    if "english" in desc or "communication" in desc:
        if any(keyword in title for keyword in [
            "executive assistant",
            "admin assistant",
            "administrative assistant",
            "virtual assistant",  # Add new keywords here
        ]):
            valid_jobs.append(row)
```

### Changing Target Website

To scrape from a different job board:

1. Update the URL in `scraper.py`
2. Modify CSS selectors/XPath to match the new site's structure
3. Update field extraction logic accordingly

## Customizing LLM Prompts

### Modifying Message Tone

Edit `outreach.py` to change available tones:

```python
tones = ["professional", "personalized", "enthusiastic", "formal"]
```

### Customizing the Prompt Template

In `outreach.py`, modify the prompt structure:

```python
prompt = f"""
Write a {tone} outreach message to the hiring manager for the following job.

Job Title: {row['Job Title']}
Company Name: {row['Company']}
Location: {row['Location']}
Job Description: {row['Job Description']}

Keep the message concise (3–4 sentences), engaging, and express genuine interest.

Additional instructions:
- Highlight relevant skills
- Show enthusiasm for the company
- Include a call to action
"""
```

### Changing AI Model

Switch between Gemini models in `outreach.py`:

```python
response = client.models.generate_content(
    model="gemini-flash-latest",  # or "gemini-2.0-flash-exp", "gemini-pro"
    contents=prompt
)
```

### Adding Message Variations

Create different prompt templates for different scenarios:

```python
if "senior" in row['Job Title'].lower():
    prompt = f"Write an executive-level outreach message..."
else:
    prompt = f"Write an entry-level outreach message..."
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Scraper Not Finding Elements

**Problem**: `NoSuchElementException` or elements not found

**Solution**:
- Website structure may have changed - inspect the site and update selectors
- Add wait times: `self.wait_for_element("selector", timeout=10)`
- Run without headless mode to see what's happening: `pytest -s scraper.py`

#### 2. Google Sheets Authentication Failed

**Problem**: `gspread.exceptions.APIError` or authentication errors

**Solution**:
- Verify `bulkread_google_sheets.json` is in the project root
- Check that APIs are enabled in Google Cloud Console
- Ensure the service account email has access to your Google Sheet
- Verify the sheet name matches exactly in `gsheet_integration.py`

#### 3. Gemini API Errors

**Problem**: API key errors or rate limiting

**Solution**:
- Verify API key in `.env` file
- Check API key is valid at [Google AI Studio](https://makersuite.google.com/)
- If rate limited, add delays between requests:
  ```python
  import time
  time.sleep(2)  # Wait 2 seconds between API calls
  ```

#### 4. No Jobs Found After Validation

**Problem**: `validated_jobs.csv` is empty

**Solution**:
- Check validation criteria in `validate.py` - they might be too strict
- Review scraped data in `All_jobs.csv` to see what was captured
- Temporarily comment out validation rules to see which one is filtering everything out
- Check for case sensitivity issues in the validation logic

#### 5. Scheduler Not Running

**Problem**: Daily execution not happening

**Solution**:
- For Python scheduler: Ensure the script is running continuously
- For cron: Check cron logs: `grep CRON /var/log/syslog`
- Verify paths in cron job are absolute paths
- Check permissions: `chmod +x scheduler.py`
- Test manually first: `python scheduler.py`

#### 6. CSV Encoding Issues

**Problem**: Special characters not displaying correctly

**Solution**:
```python
df.to_csv(filename, index=False, encoding='utf-8-sig')
```

#### 7. Memory Issues with Large Scrapes

**Problem**: Script crashes when scraping many pages

**Solution**:
- Reduce `total_pages` limit
- Process and save data in batches
- Close browser tabs more frequently

### Debug Mode

Enable verbose logging by adding print statements:

```python
# In scraper.py
print(f"Current URL: {self.get_current_url()}")
print(f"Page source length: {len(self.get_page_source())}")

# In validate.py
print(f"Processing job: {row['Job Title']}")
print(f"Location: {location}, Remote check: {'remote' in location}")
```

### Getting Help

If you encounter issues not covered here:

1. Check the log files in `logs/` directory
2. Run components individually to isolate the problem
3. Enable debug mode and capture detailed error messages
4. Verify all API keys and credentials are correct
5. Ensure all dependencies are installed: `pip list`

## Output Files

The pipeline generates the following files:

- `timesjobs_Executive_Assistants.csv` - Raw scraped data
- `timesjobs_Admin_Assistants.csv` - Raw scraped data
- `All_jobs.csv` - Combined jobs before validation
- `validated_jobs1.csv` - Filtered jobs that meet criteria
- `jobs_with_messages.csv` - Final output with AI-generated messages
- `logs/scheduler.log` - Execution logs (if using cron)

## Best Practices

1. **Test Before Scheduling**: Always run the pipeline manually first
2. **Monitor Logs**: Regularly check log files for errors
3. **Backup Data**: Keep backups of your CSV files
4. **API Rate Limits**: Be mindful of Gemini API quotas
5. **Update Selectors**: Website structures change - update selectors as needed
6. **Version Control**: Use git to track changes to your configuration
