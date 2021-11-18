import os
import requests
import re
import time
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver

import pdfplumber
import string
import json

def nv_scrape(webscrape_links, dir_chrome_webdriver, dir_save):
    
    """
    Webscrape function for Nevada State Legislature Website. 
    
    Parameters
    ----------
    webscrape_links : LIST
        List of direct link(s) to NV committee webpage.
        see nv_weblinks.py for lists organized by chamber and committee
    dir_chrome_webdriver : STRING
        Local directory that has Chrome Webdriver.
    dir_save : STRING
        Local directory to save pdfs (need to figure out file management).

    Returns
    -------
    All PDF files found on the webscrape_links, saved on local dir_save.
    
    """
    
    for link_index in range(len(webscrape_links)):
        driver=webdriver.Chrome(dir_chrome_webdriver)
        time.sleep(5)
        driver.get(webscrape_links[link_index]) 
        time.sleep(5)
        
        arrow01 = driver.find_element_by_id('divCommitteePageMeetings')
        arrow01.click()
        time.sleep(5)
    
        arrow02 = driver.find_element_by_id('divMeetings')
        arrow02.click()

        url = driver.page_source
        REGEX_PATTERN = r'https.*Minutes.*\.pdf'
        lines = url.split()
        meeting_regex = re.compile(REGEX_PATTERN)
        all_files = []
        
        for l in lines:
            hit = meeting_regex.findall(l)
            if hit:
                all_files.extend(hit)
                
        for filename in all_files:
            print(filename)
    
        folder_location = dir_save

        for link in all_files:
            filename = os.path.join(folder_location,"_".join(link.split('/')[4:]))
            urllib.request.urlretrieve(link, filename)
        time.sleep(30)
        
        driver.close()
        
def nv_pdftotext(dir_load, nv_json_name):
    """
    Convert all PDFs to a dictionary and then saved locally as a JSON file.
    
    Parameters
    ----------
    dir_load : STRING
        Local location of the directory holding PDFs.
    nv_json_name : STRING
        JSON file name, include full local path.

    Returns
    -------
    A single JSON file, can be loaded as dictionary to work with.

    """
    directory = dir_load
    n=0
    committee = {} 
    
    file_list = os.listdir(directory)
    file_list.sort()
    del file_list[0]
    
    for file in file_list:
        filename = directory + file
        all_text = '' 
        with pdfplumber.open(filename) as pdf:
            for pdf_page in pdf.pages:
                single_page_text = pdf_page.extract_text()
                all_text = all_text + '\n' + single_page_text
                committee[n]=all_text
        n=n+1   
                                
    with open(nv_json_name, 'w') as f: 
        json.dump(committee, f, ensure_ascii=False)
   
    
""" UNIT TEST

K NOTES (11/8): 
    Need to check Chrome version and download the right Chromedriver. 
    Need to print chrome version and direct people to find the right driver
    https://chromedriver.chromium.org/downloads
    I'm running Chrome Version 95 
    
    Func runs and works, I'm gettting depreciation warnings. Look into updating the functions 
    
    v_scrape(ed_test, chrome_webdriver, save_folder)
/var/folders/vp/kyx63ql12dggnl_3zsdqpsh80000gn/T/ipykernel_4733/575717094.py:11: 
    DeprecationWarning: executable_path has been deprecated, please pass in a Service object
  driver=webdriver.Chrome(dir_chrome_webdriver)
/var/folders/vp/kyx63ql12dggnl_3zsdqpsh80000gn/T/ipykernel_4733/575717094.py:16: 
    DeprecationWarning: find_element_by_* commands are deprecated. Please use find_element() instead
  arrow01 = driver.find_element_by_id('divCommitteePageMeetings')
/var/folders/vp/kyx63ql12dggnl_3zsdqpsh80000gn/T/ipykernel_4733/575717094.py:20: 
    DeprecationWarning: find_element_by_* commands are deprecated. Please use find_element() instead
  arrow02 = driver.find_element_by_id('divMeetings')
  
  Added pdftotext function, it runs but some issues
  - There are some conflicts between the save_folder in nv_scrape and the pdf_folder in nv_pdftotext', specifically need to have a / at end of pdf_folder
  - If there's a file that's NOT a PDF in the folder, it throws an error. Need to add functionality to check if the file is a PDF, and if not, then to skip it
  - Saves file not as established by json_name, but nv_leg_committee instead
  - Need to clean up directory names so they're generalizable/universal to users

"""

ed_test=["https://www.leg.state.nv.us/App/NELIS/REL/81st2021/Committee/342/Meetings"]
chrome_webdriver="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/chromedriver"
save_folder="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/toy"

pdf_folder="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/toy/" #need / at the end of folder here
json_name = "/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/toy/nv_ed.json"

nv_scrape(ed_test, chrome_webdriver, save_folder)
nv_pdftotext(pdf_folder, json_name)

with open("/Users/katherinechang/nv_leg_committee.json") as leg_json:
    committee_dict = json.load(leg_json)
