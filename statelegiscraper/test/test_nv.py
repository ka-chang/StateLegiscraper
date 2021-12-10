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
"""

import json
import os
import unittest

from statelegiscraper.states.nv import Process
from statelegiscraper.states.nv import Scrape

# Test Data

test_sen_ed = [
    "https://www.leg.state.nv.us/App/NELIS/REL/81st2021/Committee/342/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/80th2019/Committee/216/Meetings"]

test_chrome_webdriver = "statelegiscraper/assets/chromedriver/chromedriver_v96_m1"

test_save_folder = "statelegiscraper/test/outputs/"

# Unit tests by class

class TestScrape(unittest.TestCase):
    """
    Class of unittests for states.nv module, NVScrape class

    nv_scrape_pdf

    Notes: Need to test Selenium for the chrome driver used.
    Difference between the Chrome version as well as driver type (intel_64 vs. M1 for macOS; windows?)

    Make sure directories are in the proper place to save locally

    """

    def test_nv_scrape_pdf(self):
        """
        Scrape PDF using the nv_scrape_pdf function
        using test_chrome_webdriver in repo and saving outputs locally in test/outputs
        """
        Scrape.nv_scrape_pdf(test_sen_ed, test_chrome_webdriver, test_save_folder)
        test_save_folder_list = os.listdir(test_save_folder)
        #test_save_folder_filenum = len(test_save_folder_list)
        assert isinstance(test_sen_ed, list)
        assert len(test_save_folder_list) > 0 # check to make sure there are files in the output folder
        self.assertTrue(True)
        
        # assert isinstance(test_chrome_webdriver, ) #how to check it's a valid
        # chromedriver?


class TestProcess(unittest.TestCase):
    """
    Class of unittests for states.nv module, NVProcess class

    nv_pdf_to_text
    nv_text_clean
    """

    def test_nv_pdf_to_text(self):
        """
        Taking output PDFs and converting them to text
        """
        test_nv_json_path = os.path.join(test_save_folder, "test_nv_json.json")  
        test_save_folder_list = os.listdir(test_save_folder)
        assert len(test_save_folder_list) > 0  # check to make sure there are files in the 
        
        Process.nv_pdf_to_text(test_save_folder, test_nv_json_path)
        
        test_file_path = open(test_nv_json_path,)
        test_nv_dict = json.load(test_file_path)
        
        assert isinstance(test_nv_dict, dict)
        self.assertTrue(True)


#    def test_nv_text_clean(self):
#       """
#        JSON
#        """
#        Process.nv_text_clean(nv_json_path, trim=None)
#        assert isinstance(data, dict)
#        self.assertTrue(True)
