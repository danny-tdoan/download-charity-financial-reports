# Overview
This program is used to download financial reports of charity organizations from <https://www.acnc.gov.au/>.

The download is carried out in 3 phases:
1. Phase 1: Use the list of ABNs, download the info page of each charity from http://www.acnc.gov.au/
2. Phase 2: Use BeautifulSoup to extract the PDF links from each info page
3. Phase 3: Download the financial reports of the year 2014 and 2015, rename and organize

# Usage
You need to get the list of all ABNs of the charity organizations you want to download.

Please refer to `main.py` for more details.

1. Prepare the curl commands to search for the organization from ACNC
2. Use the functions in `extract_download_link` to extract the official ACNC link of the organization from the search result. Download the page.
3. Use the functions in `download_reports.py` to extract the PDF links of the reports. Download the PDF and classify it by year and organization. 