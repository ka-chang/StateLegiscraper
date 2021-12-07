"""

UNIT TEST NOTES

K NOTES (11/8):
    Need to check Chrome version and download the right Chromedriver.
    Need to print chrome version and direct people to find the right driver
    https://chromedriver.chromium.org/downloads
    I'm running Chrome Version 95

  Added pdftotext function, it runs but some issues
  - There are some conflicts between the save_folder in nv_scrape and the pdf_folder in nv_pdftotext', specifically need to have a / at end of pdf_folder
  - If there's a file that's NOT a PDF in the folder, it throws an error. Need to add functionality to check if the file is a PDF, and if not, then to skip it
  - Saves file not as established by json_name, but nv_leg_committee instead
  - Need to clean up directory names so they're generalizable/universal to users

ed_test=["https://www.leg.state.nv.us/App/NELIS/REL/81st2021/Committee/342/Meetings"]
chrome_webdriver="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/chromedriver"
save_folder="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/toy"

pdf_folder="/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/toy/" #need / at the end of folder here
json_name = "/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/toy/nv_ed.json"

nv_scrape(ed_test, chrome_webdriver, save_folder)
nv_pdftotext(pdf_folder, json_name)

with open("/Users/katherinechang/nv_leg_committee.json") as leg_json:
    committee_dict = json.load(leg_json)

"""

import os
import sys
import unittest

from LegTextScraper.states.nv import NVScrape
from LegTextScraper.states.nv import NVProcess

# Test Data

test_sen_ed = [
    "https://www.leg.state.nv.us/App/NELIS/REL/81st2021/Committee/342/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/80th2019/Committee/216/Meetings"]

test_chrome_webdriver = "test/chromedriver_m1"

test_save_folder = "test/outputs"


class TestNVScrape(unittest.TestCase):
    """
    Class of unittests for states.nv module, NVScrape class

    nv_scrape_pdf

    Notes: Need to test Selenium for the chrome driver used.
    Difference between the Chrome version as well as driver type (intel_64 vs. M1 for macOS; windows?)

    Make sure directories are in the proper place to save locally

    """

    def test_nv_scrape_pdf(
            test_sen_ed, test_chrome_webdriver, test_save_folder):
        """
        Scrape PDF using the nv_scrape_pdf function
        using test_chrome_webdriver in repo and saving outputs locally in test/outputs
        """
        nv_scrape_pdf(test_sen_ed, test_chrome_webdriver, test_save_folder)
        assert isinstance(test_sen_ed, list)
        # assert isinstance(test_chrome_webdriver, ) #how to check it's a valid
        # chromedriver?
        # Check number of files in the output folder to ensure it's the right
        # number of files
        assert len(test_save_folder) > 0


class TestNVProcess(unittest.TestCase):
    """
    Class of unittests for states.nv module, NVProcess class

    nv_pdf_to_text
    nv_text_clean
    """

    def test_nv_pdf_to_text(dir_load, nv_json_name):
        """
        Taking output PDFs and converting them to text
        """
        nv_pdf_to_text(dir_load, nv_json_name)
        assert len(dir_load) > 0  # check to make sure the
        assert isinstance(nv_json_name, dict)

    def test_nv_text_clean(nv_json_path):
        """
        JSON
        """
        nv_text_clean(nv_json_path, trim=None)
        assert isinstance(data, dict)
