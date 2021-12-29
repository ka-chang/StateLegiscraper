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

#Contained state for unit tests, using dummy data

#Contained state for unit tests, integrate data that are directly downloaded

#Integration state for unit tests, using live data
# -Can it connect to the website?
# -Does the driver work?
# -Can it navigate through click actions?
# -Has the format of the website changed?
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
    Class of unittests for states.nv module, Scrape class

    nv_scrape_pdf

    Notes: Need to test Selenium for the chrome driver used.
    Difference between the Chrome version as well as driver type (intel_64 vs. M1 for macOS; windows?)

    Make sure directories are in the proper place to save locally

    """

    def test_nv_scrape_01_list(self):
        """
        Parameter 1 Test: Make sure test_sen_ed is a list
        """
        self.assertIsInstance(test_sen_ed, list)

    def test_nv_scrape_02_driver(self):
        """
        Parameter 2 Test: Make sure test_chrome_webdriver points to a file

        Notes: Eventually need to check that it's the appropriate webdriver file for the user hardware
        """
        self.assertIsFile(test_chrome_webdriver)

    def test_nv_scrape_03_folder(self):
        """
        Parameter 3 Test: Make sure test_save_folder points to a file
        """
        self.assertIsFile(test_save_folder)

    def test_nv_scrape_04_pdf(self):
        """
        Function Test: Scrape PDF using the nv_scrape_pdf function
        using test_chrome_webdriver in repo and saving outputs locally in test/outputs
        """
        Scrape.nv_scrape_pdf(
            test_sen_ed,
            test_chrome_webdriver,
            test_save_folder)
        test_save_folder_list = os.listdir(test_save_folder)
        # check to make sure there are files in the output folder
        self.assertTrue(len(test_save_folder_list) > 0)
        # self.assertGreater(len (...), 0)
        # #https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertGreater


class TestProcess(unittest.TestCase):
    """
    Class of unittests for states.nv module, Process class

    nv_pdf_to_text
    nv_text_clean
    """

    def test_nv_process_01_folder(self):
        """
        Parameter 1 Test: Make sure there are files in test_save_folder
        """
        test_save_folder_list = os.listdir(test_save_folder)
        assert len(test_save_folder_list) > 0

    def test_nv_process_02_json(self):
        """
        Parameter 2 Test: Make sure JSON path is a string
        """
        test_nv_json_path = os.path.join(test_save_folder, "test_nv_json.json")
        self.assertIsInstance(test_nv_json_path, str)

    def test_nv_process_03_pdf_to_text(self):
        """
        Function Test: Run pdf_to_text function, test_nv_json_path should be file now, not just string
        """
        test_nv_json_path = os.path.join(test_save_folder, "test_nv_json.json")
        Process.nv_pdf_to_text(test_save_folder, test_nv_json_path)

        self.assertIsFile(test_nv_json_path)

    def test_nv_process_04_json_dump(self):
        """
        Object Test: Load JSON file as a dictionary and check object type
        """
        test_nv_json_path = os.path.join(test_save_folder, "test_nv_json.json")

        test_file_path = open(test_nv_json_path,)
        test_nv_dict_raw = json.load(test_file_path)

        self.assertIsInstance(test_nv_dict_raw, dict)

    def test_nv_process_clean_untrimmed(self):
        """
        Function Test: Run nv_text_clean function, test_nv_json_path should be file now, not just string
        """
        test_nv_json_path = os.path.join(test_save_folder, "test_nv_json.json")
        test_nv_dict_untrimmed = Process.nv_text_clean(test_nv_json_path)

        self.assertIsInstance(test_nv_dict_untrimmed, dict)

    def test_nv_process_clean_trimmed(self):
        """
        Function Test: Run nv_text_clean function, test_nv_json_path should be file now, not just string
        """
        test_nv_json_path = os.path.join(test_save_folder, "test_nv_json.json")
        test_nv_dict_trimmed = Process.nv_text_clean(
            test_nv_json_path, trim=True)

        self.assertIsInstance(test_nv_dict_trimmed, dict)
