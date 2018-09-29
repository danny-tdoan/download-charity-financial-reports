from bs4 import BeautifulSoup
from constants import *
import os
import re
import urllib.request as ur


def extract_pdf_link(file, abn_to_download, abn_existed):
    """Search for the PDF links and download the financial reports, rename the report to the format {abn}_{year}.pdf
    The function update links that are completed, to allow it to resume to the last checkpoints in the future (in case
    there are connection errors, disruptions)"""
    content = open(file).read()
    soup = BeautifulSoup(content)

    # extract the ABN
    try:
        abn = soup.find('a', href=re.compile('^http://www.abr.business.gov.au/SearchByAbn.aspx')).text

        # download all remaining charities
        if abn in abn_to_download and abn not in abn_existed:
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

            abn_existed.append(abn)

            fh = open(FINAL_OUTPUT + 'abn_pdf_downloaded.txt', 'a')
            fh.write(abn + '\n')
            fh.close()

    except Exception:
        print('something wrong with ' + file)
