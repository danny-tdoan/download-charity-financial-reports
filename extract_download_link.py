from bs4 import BeautifulSoup
import sys
import os
import re
import urllib.request as ur
from constants import *


def extract_urls_from_file(f, all_abns, links_existed):
    """This function analyzes the result of the search page to extract the URL link that points to the page
    of the charity organization.
    Input: <the first line of the curl_queries> (for ABN 63006186812)

    Output: https://www.acnc.gov.au/RN52B75Q?ID=A2274991-E97B-4D76-8473-153CE3405A1F&noleft=1
    """
    content = open(CURL_OUTPUT + f).read()
    soup = BeautifulSoup(content)

    fh = open(ALL_LINKS + 'all_links.txt', 'a')

    cnt = 0
    all_rows = soup.find_all('tr', {'class': 'rgRow'})
    for row in all_rows:
        all_cells = row.find_all('td')
        abn = all_cells[0].text
        if (abn in all_abns):
            link = all_cells[1].findChildren('a')[0]['href']
            if not link in links_existed:
                print(link)
                download_page(link, f, cnt)
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
