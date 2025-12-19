from seleniumbase import BaseCase
BaseCase.main(__name__, __file__)


class RecorderTest(BaseCase):
    def test_recording(self):
        self.open("https://www.timesjobs.com/")
        self.open("about:blank")
        self.open("https://www.timesjobs.com/")
        self.type('input[placeholder="Enter Skills, Designation, etc"]', "administrative ")
        self.click('li:contains("Administrative Assistant")')
        self.click('button:contains("Let\'s Find")')
        self.open_if_not_url('https://www.timesjobs.com/job-search?keywords="Administrative+Assistant",&location=&experience=&refreshed=true')
        self.open("about:blank")
        self.open('https://www.timesjobs.com/job-search?keywords="Administrative+Assistant",&location=&experience=&refreshed=true')
        self.open("https://www.timesjobs.com/job-detail/urgent-opening-for-executive-assistant-to-director-universal-consultant-and-management-services-kolkata-3-8-years-jobid-u__SLASH____SLASH__wMjXE3fJzpSvf+uAgZw==&source=srp")
        self.click("button.pagination-next")
        self.click("button.pagination-next")
