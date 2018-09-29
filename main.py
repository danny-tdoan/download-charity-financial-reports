"""Download the financial reports of all charity organization for the years of 2014 and 2015.
The procedure is divided into 3 phases:
    Phase 1: Use the list of ABNs, download the info page of each charity from http://www.acnc.gov.au/
    Phase 2: Use BeautifulSoup to extract the PDF links from each info page
    Phase 3: Download the financial reports of the year 2014 and 2015, rename and organize

The analyzed content is stored at each phase, to allow the downloader to resume later in case of disruption/errors
"""
import os
from constants import *
from utilities import extract_pdf_link, extract_urls_from_file

# Update this to skip a phase
starting_phase = 2

# Resume from the last abn
all_abns = open(DATA_LOC + 'all_abns.txt').read().split()

if starting_phase == 1:
    print("Starting phase 1...")

    # Retrieve the status of curl links
    try:
        abn_existed_curl = open(DATA_LOC + 'abn_existed_curl.txt').read().split()
    except FileNotFoundError:
        # first time running
        abn_existed_curl = []
        fh_existed = open(DATA_LOC + 'abn_existed_curl.txt', 'w')

    # Remaining abns that need to have curl prepared
    remaining_abn_curl = list(set(all_abns) - set(abn_existed_curl))

    fh = open(CURL_OUTPUT + 'curl_queries.cmd', 'w')
    for abn in remaining_abn_curl:
        curl_command = CURL_TEMPLATE.format(ABN_GOES_HERE=abn)
        curl_command = curl_command + ' > ' + abn + '.htm'
        fh.write(curl_command + '\n')

        abn_existed_curl.append(abn)
        fh_existed.write(abn + "\n")

    fh.close()
    fh_existed.close()

    # execute the curl to download the file
    # easiest to run this in bash separately rather than use pycurl
    os.system(CURL_OUTPUT + 'curl_queries.cmd')

if starting_phase <= 2:
    print("Starting phase 2...")

    try:
        abn_existed_links = open(DATA_LOC + 'abn_existed_links.txt').read().split()
    except FileNotFoundError:
        # first time running
        abn_existed_links = []
        fh_existed = open(DATA_LOC + 'abn_existed_links.txt', 'w')

    for file in os.listdir(CURL_OUTPUT):
        abn = file.split('.')[0]
        if file.endswith(".htm") and abn not in abn_existed_links:
            extract_urls_from_file(file)

            abn_existed_links.append(abn)
            fh_existed.write(abn + "\n")

    fh_existed.close()

if starting_phase <= 3:
    print("Starting phase 3...")
    try:
        abn_pdf_downloaded = open(FINAL_OUTPUT + 'abn_pdf_downloaded.txt', 'r').read().split()
    except FileNotFoundError:
        abn_pdf_downloaded = []
        fh_downloaded =open(FINAL_OUTPUT + 'abn_pdf_downloaded.txt', 'w')

    for file in os.listdir(ALL_PAGES):
        abn=file.split('.')[0]
        if file.endswith(".htm") and abn not in abn_pdf_downloaded:
            extract_pdf_link(ALL_PAGES + file)

            abn_pdf_downloaded.append(abn)
            fh_downloaded.writable(abn+"\n")

    fh_downloaded.close()
