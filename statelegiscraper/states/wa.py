"""
WA module for scraping and processing text from https://leg.wa.gov 

# Status

Current Coverage (In Active Development):
    [ ] Committee Hearings (Audio Links) (2015 - 2020)

Planned Coverage:
    [ ] Committee Hearings (Video Links) (2000 - 2014)
    [ ] Floor Speeches (Video Links)

# WA Work Flow

CLASS WAScrape

    - wa_scrape_meeting_links by desired committee and legislative session. 
    Function searches TVW archives for links to each individual committee meeting for that leg session
    
    - wa_scrape_audio by wa_meeting_links output (or custom output in weblinks form)
    Function visits each link individually and gather weblinks for each meeting hearing audio by mp3 link on page
    Pulls input by wa_scrape_audio for the weblinks by desired committee and leg session
    Rename the file names by committee name and date (YYYYMMDD) (e.g. wa_education_20200305.mp3)

CLASS WAProcess

    - wa_speech_to_text
    Function gives the user option to convert audio file to a text transcript through DeepSpeech
    Uses mp3 links directly to process the transcripts
    Downloads the transcript in json form, single json for each committee/legislative session
    
    - wa_text_clean
    Function conducts tests and run light cleaning to ensure transcript is ready for text analysis

"""

import os
from pathlib import Path
import sys
import re
import time

import urllib.request
from urllib.parse import urljoin

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

print(selenium.getsitepackages()[0])


class Scrape:
    """
    """


def wa_meeting_links():

  """
  """
  
# DRIVER SETUP
service = Service("/Users/katherinechang/Google Drive/My Drive/State Legislatures/StateLegiscraper/statelegiscraper/assets/chromedriver/chromedriver_v96_m1")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

####

# OPEN TO TVW ARCHIVES 
driver.get("https://tvw.org/video-search/")

# CLICK CATEGORIES TO OPEN 
driver.find_element(By.CLASS_NAME, "MuiGrid-grid-xs-12").click()

# INPUT COMMITTEE NAME
input_search = driver.find_element(By.XPATH, "//input[contains(@class, 'MuiInputBase-input MuiInput-input')]")
input_search.send_keys("House Education")

# SELECT COMMITTEE NAME FROM DROP DOWN
driver.find_element(By.XPATH, "//div[@class='MuiListItemText-root jss3 jss4 MuiListItemText-multiline' and @title='House Education']").click()

# SELECT START DATE BY LEGISLATIVE SESSION

driver.find_element(By.XPATH, "//div[@class='react-datepicker__input-container']").click() #Calendar dropdown
driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").click() #Year dropdown

year_list = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")

if parameter_year == "2020":
    year_list[0].click() #2020
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
    "Incompatiable Year, Current coverage only includes 2015 to 2020"
    
driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--001']").click() #The 1st of the month


#MONTH
#driver.find_elements(By.XPATH, "//div[@class='react-datepicker__month-container']")
#driver.find_element(By.XPATH, "//div[@class='react-datepicker__month-container']").click()
#driver.find_element(By.XPATH, "//div[@class='react-datepicker__navigation react-datepicker__navigation--previous']")

#JAVASCRIPT OPTION (DOESN'T STICK)
#start_date = driver.find_element(By.XPATH, "//input[@class='css-13hc3dd']")
#driver.execute_script("arguments[0].value = arguments[1]", start_date, "08/05/2018") #input date, but doesn't stick

# SELECT END DATE BY LEGISLATIVE SESSION

#end_date = driver.find_element(By.XPATH, "//input[@class='css-13hc3dd']")
#driver.execute_script("arguments[0].value = arguments[1]", start_date, "08/05/2020") #input date, but doesn't stick

# PRESS SUBMIT 
driver.find_element(By.XPATH, "//button[@class='filter__form-submit css-1l4j2co']").click()

####

# SAVE LINKS FOR MULTIPLE PAGES

url = driver.page_source

# FOR EACH PAGE SEARCH FOR A HREF TAG TO CREATE A LIST OF WEBLINKS, AUDIO ENDS WITH .MP3

match = re.search(r'href=[\'"]?([^\'" >]+)', lines)

for i in lines:
    hit = meeting_regex.findall(l)

REGEX_PATTERN = r".*(\?eventID\=).*"
lines = url.split()
meeting_regex = re.compile(REGEX_PATTERN)
all_files = []

for l in lines:
    hit = meeting_regex.findall(l)
    if hit:
        print(hit)
        #all_files.extend(hit)
        
for filename in all_files:
    print(filename)

<a href="/watch/?eventID=2021111051">

# GO THROUGH EACH PAGE AND GATHER THE LINKS TO EACH MEETING

driver.close()



    def wa_scrape_audio():
    
      """
        Webscrape function for Washington State Legislature Website for 2016-2020 sessions 
        
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
    
        service = Service("/Users/katherinechang/Google Drive/My Drive/2021/Fall 2021/CSE583/project/chromedriver_m1")
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(service=service, options=options)
        
        #Loop here to visit each link for the webscrape_links object
        
        driver.get("https://www.tvw.org/watch/?eventID=2021021259") 
        driver.find_element(By.ID, 'content').click()
        
        url = driver.page_source
        REGEX_PATTERN = r'https.*audio.*\.mp3'
        lines = url.split()
        meeting_regex = re.compile(REGEX_PATTERN)
        mp3_files = []
        
        for l in lines:
            hit = meeting_regex.findall(l)
            if hit:
                mp3_files.extend(hit)
                
        for filename in mp3_files:
            print(filename)
        
        driver.close()
        
        #Option to download if true
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
