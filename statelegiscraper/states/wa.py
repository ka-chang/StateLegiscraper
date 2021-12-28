"""
WA module for scraping and processing text from https://leg.wa.gov 

# Status

Current Coverage (In Active Development):
    [X] Committee Hearings (Audio Links) (2015 - 2020)

Planned Coverage:
    [ ] Committee Hearings (Video Links) (2000 - 2014)
    [ ] Floor Speeches (Video Links)

# WA Work Flow

CLASS Scrape

    - wa_scrape_links by desired committee and legislative session. 
    Function filters TVW archives by function parameters
    for links to each individual committee meeting for that calendar year
    
    - wa_scrape_audio by wa_scrape_links output 
    Function downloads audio files to local drive
    Renames the file names by committee name and date (YYYYMMDD) (e.g. wa_education_20200305.mp3)

CLASS Process

    - wa_speech_to_text
    Function gives the user option to convert audio file to a text transcript through DeepSpeech
    Uses mp3 links directly to process the transcripts
    Downloads the transcript in json form, single json for each committee/legislative session
    
    - wa_text_clean
    Function conducts tests and run light cleaning to ensure transcript is ready for text analysis

"""

from datetime import datetime
import os
import sys
import re
import time

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

#TESTING 

dir_chrome_webdriver = "/Users/katherinechang/Google Drive/My Drive/State Legislatures/StateLegiscraper/statelegiscraper/assets/chromedriver/chromedriver_v96_m1"

class Scrape:
    """
    Scrape functions for Washington State Legislature website
    Current coverage includes committee hearing audio links 
    """

    def wa_scrape_links(param_committee, param_year, dir_chrome_webdriver, dir_save):
        """
        Webscrape function for Washington State Legislature Website for 2015-2020 sessions 
        
        Parameters
        ----------
        param_committee : String
            Standing committee hearing name (see list with "xxx").
        param_year : String
            Calendar year (Current coverage limited to 2015-2021).
        dir_chrome_webdriver : String
            Local directory that contains the appropriate Chrome Webdriver.
        dir_save : String
            Local directory to save JSON with audio links.
    
        Returns
        -------
        A JSON file saved locally with selected committee and year audio files
    
        """
        
        if not isinstance(param_committee, string):
            raise ValueError("Committee name must be a string")
        else:
            pass

        if not isinstance(param_year, string):
            raise ValueError("Year selection must be a string")
        else:
            pass

        if not os.path.exists(dir_chrome_webdriver):
            raise ValueError("Chrome Webdriver not found")
        else:
            pass

        if not os.path.exists(dir_save):
            raise ValueError("Save directory not found")
        else:
            pass
  
        # DRIVER SETUP
        service = Service(dir_chrome_webdriver)
        options = webdriver.ChromeOptions()
        # Chrome runs headless, 
        # comment out "options.add_argument('headless')"
        # to see the action
        # options.add_argument('headless')
        driver = webdriver.Chrome(service=service, options=options)
        
        ####
        
        # OPEN TO TVW ARCHIVES 
        driver.get("https://tvw.org/video-search/")
        time.sleep(5)
        
        # CLICK CATEGORIES TO OPEN 
        driver.find_element(By.CLASS_NAME, "MuiGrid-grid-xs-12").click()
        
        # INPUT COMMITTEE NAME
        input_search = driver.find_element(By.XPATH, "//input[contains(@class, 'MuiInputBase-input MuiInput-input')]")
        input_search.send_keys("House Education")
        
        # SELECT COMMITTEE NAME FROM DROP DOWN
        driver.find_element(By.XPATH, "//div[@class='MuiListItemText-root jss3 jss4 MuiListItemText-multiline' and @title='House Education']").click()
        
        # SELECT START DATE BY LEGISLATIVE SESSION
        
        """ Javascript Option, more efficient/accurate solution but needs debugging, issue with flex object
        #OPTION 1: Can change date value for input, but flex resets it to default/current date when submitted 
        date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        start_date = date_elements[0]
        end_date = date_elements[1]
        driver.execute_script("arguments[0].value = 12/27/2015", start_date)
        
        #OPTION 2: Can change entire input-container innerHTML, but site crashes when submitted
        date_elements = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__input-container']")
        start_html = date_elements[0].get_attribute("innerHTML")
        start_date = date_elements[0]
        end_html = date_elements[1].get_attribute("innerHTML")
        end_date = date_elements[1]
        
        start_script = '<div class="css-1s0fs6f"><input class="css-13hc3dd" value="12/27/2015"></div>'
        
        driver.execute_script("arguments[0].innerHTML = arguments[1]", start_date, start_script)
        """
        
        """ Interactive Option, simulate clicks on the search form. Works but clunky.
        """
        
        # SELECT START AND END MONTH (JANUARY - DECEMBER)
        # Date is reliant on current date, start month set to January 1st of cal year
        driver.find_element(By.XPATH, "//div[@class='react-datepicker__input-container']").click() #Calendar dropdown
        
        date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        start_date = date_elements[0].get_attribute("value")
        end_date = date_elements[1].get_attribute("value")
        start_datetime = datetime.strptime(start_date, '%m/%d/%Y').date()
        end_datetime = datetime.strptime(end_date, '%m/%d/%Y').date()
        
        def _loop_month():
            driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--001']").click() 
            date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
            loop_date = date_elements[0].get_attribute("value")
            loop_datetime = datetime.strptime(loop_date, '%m/%d/%Y').date()
            assert loop_datetime.month == 1, "Month set to January"
        
        previous_month_click = "//button[@class='react-datepicker__navigation react-datepicker__navigation--previous']"
        
        if start_datetime.month == 12:
            for i in range(0,11):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 11:
            for i in range(0,10):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 10:
            for i in range(0,9):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 9:
            for i in range(0,8):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 8:
            for i in range(0,7):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 7:
            for i in range(0,6):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 6:
            for i in range(0,5):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 5:
            for i in range(0,4):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 4:
            for i in range(0,3):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 3:
            for i in range(0,2):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 2:
            for i in range(0,1):
                driver.find_element(By.XPATH, previous_month_click).click()
                i+=1
            _loop_month()
        elif start_datetime.month == 1:
            _loop_month()
        else:
            print("Invalid Date")
            
        # SELECT START YEAR (ESTABLISHED BY PARAM_YEAR)
        
        date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        year_date = date_elements[0].get_attribute("value")
        year_datetime = datetime.strptime(year_date, '%m/%d/%Y').date()
        
        driver.find_element(By.XPATH, "//div[@class='react-datepicker__input-container']").click()
        driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").click() #Year dropdown
        
        year_list = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")
        
        if parameter_year == "2021":
            year_list[0].click() #2021
        elif selected_year == "2020":
            pass
        elif selected_year == "2019":
            year_list[1].click() #2019
        elif selected_year == "2018":
            year_list[2].click() #2018
        elif selected_year == "2017":
            year_list[3].click() #2017
        elif selected_year == "2016":
            year_list[4].click() #2016
        elif selected_year == "2015":
            year_list[5].click() #2015
        else:
            "Invalid Year. Current coverage limited to 2015 to 2021"
        
        driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--001']").click() 
        
        driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--002']").click()
        #Sometimes the 1st lands on a weekend, in that case we need to pick the 2nd or 3rd of the month
        
        # PRESS SUBMIT 
        driver.find_element(By.XPATH, "//button[@class='filter__form-submit css-1l4j2co']").click()
        
        ####
        
        # SAVE HTML FOR MULTIPLE PAGES
        
        url_html = []
        
        url_html.append(driver.page_source) #CURRENT PAGE, PAGE 1
        
        #url_link = driver.find_element(By.XPATH, "//div[@class='pagination__Pagination-sc-gi8rtp-0 efVChy pagination']")
        #url_pages_innerhtml = url_link.get_attribute("innerHTML")
        url_page_numbers= driver.find_elements(By.XPATH, "//button[@class='pagination__Button-sc-gi8rtp-2 hFycqx pagination__button css-18u3ks8']")
        url_page_length = len(url_page_numbers)
        
        for page_num in range(url_page_length): #length + 1, since it doesn't include first page (currently loaded page)
            url_page_loop= driver.find_elements(By.XPATH, "//button[@class='pagination__Button-sc-gi8rtp-2 hFycqx pagination__button css-18u3ks8']")
            url_page_loop[page_num].click() 
            time.sleep(5)
            url_html.append(driver.page_source) 
            url_page_home= driver.find_elements(By.XPATH, "//button[@class='pagination__Button-sc-gi8rtp-2 hFycqx pagination__button css-18u3ks8']")
            url_page_home[0].click()
            time.sleep(5)
        
        assert len(url_html) > 0, "Check that there's content in the html list"
        
        driver.close()
        
        ####
        
        # FOR EACH PAGE SOURCE SEARCH FOR A HREF TAG ENDING IN .MP3 TO CREATE A LIST OF AUDIO LINKS, 
        
        committee_links=[]
        committee_dates=[]
        
        for url_page in range(len(url_html)):
            soup_html = BeautifulSoup(url_html[url_page])
            links_all = soup_html.findAll('a', href=True)
            links_mp3 = [l for l in links_all if l['href'].endswith('.mp3')]
            
            for l in links_mp3: 
                committee_links.append(l['href'])
        
            soup_divs_dates = soup_html.find_all("div", class_="table__Cell-sc-z0zx9b-7 table__Date-sc-z0zx9b-9 fZbwqH idBpML")
            for d in range(len(soup_divs_dates)):
                committee_dates.append(soup_divs_dates[d].get_text())

        assert len(committee_links) == len(committee_dates), \
            "Ensure both links and dates match before joining"

    def wa_scrape_audio():
    
      """
        Webscrape function for Washington State Legislature Website for 2015-2020 sessions 
        
        Parameters
        ----------
        webscrape_links : LIST
            List of direct link(s) to WA committee video pages.
            Can also use list generated by wa_committee_links() 
        dir_chrome_webdriver : STRING
            Local directory that has Chrome Webdriver.
        dir_save : STRING
            Local directory to save audio files
    
        Returns
        -------
        All audio files found on the webscrape_links, either as an object or saved on local dir_save.
        
        """
        
        if download:
        
            folder_location = dir_save
            
            for link in mp3_files:
                filename = os.path.join(folder_location,"_".join(link.split('/')[4:]))
                urllib.request.urlretrieve(link, filename)
        
        return(mp3_files)

#### WORK IN PROGRESS

class Process:
    """
    """
    def wa_speech_to_text(weblinks_mp3):
        """
        Function gives the user option to convert audio file to a text transcript through DeepSpeech package

        Parameters
        ----------
        weblinks_mp3 : TYPE
            DESCRIPTION.

        Returns
        -------
        Downloads the transcript in json form, single json for each committee/legislative session

        """
    
#STEP 1: Convert mp3 file to wav, 1600 frame rate, mono channel
        
        from pydub import AudioSegment
        os.chdir("/Users/katherinechang/Downloads") #Location of the saved mp3
        audio_org = "071722fb938c8e0a87505936941971725631c303_audio.mp3"
        audio_wav = "wa_house_ed_2_20_21.wav"
        sound = AudioSegment.from_mp3(audio_org)
        sound.export(audio_wav, format="wav")
        new_sound = sound.set_frame_rate(16000).set_channels(1)
        
        ## ISSUE: Converting to wav ends up with a large file size. Do it one at a time and then delete? Save the MP3s all together
        
        #audio_org = "071722fb938c8e0a87505936941971725631c303_audio.mp3" #weblinks_mp3
        #audio_wav = "wa_house_ed_2_20_21.wav"
        
        #---QUESTION: Best practices of running command line as part of functions? 
        #---QUESTION: HOW TO CALL VARIABLES TO CLI
        #!ffmpeg -i audio_org  -ar 16000 -ac 1  audio_wav
        #!ffmpeg -i 071722fb938c8e0a87505936941971725631c303_audio.mp3  -ar 16000 -ac 1 wa_house_ed_2_20_21.wav

#STEP 2: Run DeepSpeech for each converted wav file and save transcript in new output folder
#Model and vad_transcriber saved in statelegiscraper/assets 
#Depending on length, can run 15+ minutes per audio file. Should we do it one by one?

        start = time.time()
        !python3 DeepSpeech/vad_transcriber/audioTranscript_cmd.py --aggressive 1 --audio wa_house_ed_2_20_21.wav --model ./
        #Make a list of wav files, bash command constructed as an object, each iteration of the loop just replace the argumement of the flag
        #with the current value of the loop

"""
flags={"--aggressive": 1", "--audio": "filename", "--model: "./"}
for f in filenames:
  flags["--audio"] = f
  self.ExecuteThis(command, flags)
  
"""
        
        end = time.time()
        print("Total time: {:.2f}".format(end-start))

#STEP 3: Check to make sure .txt is saved
        

    def wa_text_clean(transcript):
        """

        Parameters
        ----------
        transcript : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        

"""
https://invintus-client-media.s3.amazonaws.com/9375922947/bb61b863f2ace56a560d401f1deebfc17ec0201c_audio.mp3
https://invintus-client-media.s3.amazonaws.com/9375922947/071722fb938c8e0a87505936941971725631c303_audio.mp3

NOTES:
    Audio download button available until 2016. 2015 and previous years will require video links (mp4)
"""
