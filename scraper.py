from seleniumbase import BaseCase
import pandas as pd

BaseCase.main(__name__, __file__)

class TimesJobsScraper(BaseCase):

    def test_scrape_positions(self):
        positions = ["Executive Assistants", "Admin Assistants"]
        for pos in positions:
            self.scrape_jobs_for_position(pos)
            
    def close_extra_tabs(self):
        handles = self.driver.window_handles
        while len(handles) > 1:
            self.driver.switch_to.window(handles[-1])
            self.driver.close()
            handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])

    def scrape_jobs_for_position(self, position):
        self.open("https://www.timesjobs.com/")
        self.type('input[placeholder="Enter Skills, Designation, etc"]', position)
        self.click('button:contains("Let\'s Find")')
        print(f"Search successful for position: {position}")

        # Get total pages
        pages_text = self.get_text("div.flex.justify-center.items-center.space-x-2 button:nth-child(4)")
        total_pages = int(pages_text)
        print("Total pages:", total_pages)
        total_pages = min(total_pages, 20)
        print("Pages to scrape:", total_pages)
        all_data = []

        for page_num in range(1, total_pages + 1):
            print(f"Scraping page {page_num}/{total_pages}")
            # Loop over jobs in the page
            for job_index in range(3, 12):  # adjust indices if needed
                try:
                    # Click the job listing
                    self.click(f'/html/body/div/main/div/div[1]/div/div[2]/div[{job_index}]', by="xpath")

                    # Extract fields
                    job_title = self.get_text("h1.text-lg.font-bold")
                    company = self.get_text("h3[title]")
                    posted_date = self.get_text("span.text-gray-600.text-xs")
                    location = self.get_text("span:has(i.locations-icon)")
                    experience = self.get_text("span:has(i.years-icon)")
                    salary = self.get_text("span:has(i.salary-icon)")
                    job_description = self.get_text("div.rtd-content")

                    # Key Details
                    key_details_elements = self.find_elements("div.border-b.border-gray-300 ul li")
                    key_details = {}
                    for elem in key_details_elements:
                        parts = elem.text.split(":", 1)
                        if len(parts) == 2:
                            key, value = parts
                            key_details[key.strip()] = value.strip()

                    # Key Skills
                    skills_elements = self.find_elements("div.mt-2 span.border")
                    skills = [s.text for s in skills_elements]

                    # Append data
                    all_data.append([
                        job_title,
                        company,
                        posted_date,
                        location,
                        experience,
                        salary,
                        job_description,
                        skills,
                        key_details
                    ])

                    print(f"Scraped job {job_index} on page {page_num}")

                    # Go back to search results if needed
                    self.open_if_not_url('https://www.timesjobs.com/job-search?keywords="Administrative+Assistant",&location=&experience=&refreshed=true')

                    self.close_extra_tabs()
                except Exception as e:
                    print(f"Error scraping job {job_index} on page {page_num}: {e}")
                    self.open_if_not_url('https://www.timesjobs.com/job-search?keywords="Administrative+Assistant",&location=&experience=&refreshed=true')
                    self.close_extra_tabs()

            # Go to next page
            try:
                self.click("button.pagination-next")
            except:
                print("No more pages or pagination-next button missing")

        # Save to CSV
        df = pd.DataFrame(all_data, columns=[
            "Job Title",
            "Company",
            "Posted Date",
            "Location",
            "Experience",
            "Salary",
            "Job Description",
            "Skills",
            "Key Details"
        ])
        filename = f"timesjobs_{position.replace(' ', '_')}.csv"
        df.to_csv(filename, index=False)
        print(f"Saved data to {filename}")


#pytest -s .\test_scraper.py
