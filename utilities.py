from bs4 import BeautifulSoup
import os
import re
import urllib.request as ur
from constants import *


def extract_pdf_link(file):
    """Search for the PDF links and download the financial reports, rename the report to the format {abn}_{year}.pdf
    The function update links that are completed, to allow it to resume to the last checkpoints in the future (in case
    there are connection errors, disruptions)"""
    content = open(file).read()
    soup = BeautifulSoup(content)

    # extract the ABN
    try:
        abn = soup.find('a', href=re.compile('^http://www.abr.business.gov.au/SearchByAbn.aspx')).text

        # download all remaining charities
        pdf_2014 = soup.find('a', href=True, text='Financial Report 2014')
        pdf_2015 = soup.find('a', href=True, text='Financial Report 2015')

        # download if the link does exist
        # sometime the financial report is not available (missing, or the organization is new)
        if pdf_2014:
            pdf_2014_file = ur.urlopen(URL_PREFIX + pdf_2014['href'])
            with open(FINAL_OUTPUT + abn + '_2014.pdf', 'wb') as output:
                output.write(pdf_2014_file.read())

        if pdf_2015:
            pdf_2015_file = ur.urlopen(URL_PREFIX + pdf_2015['href'])
            with open(FINAL_OUTPUT + abn + '_2015.pdf', 'wb') as output:
                output.write(pdf_2015_file.read())

        fh = open(FINAL_OUTPUT + 'abn_pdf_downloaded.txt', 'a')
        fh.write(abn + '\n')
        fh.close()

    except Exception:
        # a bit messy, note down the links that fail and retry
        print('something wrong with ' + file)


def extract_urls_from_file(file):
    """This function analyzes the result of the search page to extract the URL link that points to the page
    of the charity organization.
    Input: <the first line of the curl_queries> (for ABN 63006186812)

    Output: https://www.acnc.gov.au/RN52B75Q?ID=A2274991-E97B-4D76-8473-153CE3405A1F&noleft=1
    """
    content = open(CURL_OUTPUT + file).read()
    soup = BeautifulSoup(content)

    # conveniently save the links that have been extracted, easier to resume later
    fh = open(ALL_LINKS + 'all_links.txt', 'a')

    cnt = 0
    all_rows = soup.find_all('tr', {'class': 'rgRow'})
    for row in all_rows:
        all_cells = row.find_all('td')
        abn = all_cells[0].text

        link = all_cells[1].findChildren('a')[0]['href']

        print(link)
        download_page(link, file, cnt)
        fh.write(link + '\n')
        cnt = cnt + 1

    fh.close()


def download_page(link, f, cnt):
    """Download the page and store it in html format. The files will be analyzed to extract the link of the PDF
    financial report"""
    try:
        page = ur.urlopen(link).read().decode()
        fh = open(ALL_PAGES + f + str(cnt) + '.htm', 'w')

        fh.write(page)
        fh.close()
    except Exception:
        print('Something wrong with link ' + link)
