"""
WA module for scraping and processing text from https://leg.wa.gov 

# Status, as of January 1, 2022

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

from collections import OrderedDict
from datetime import datetime
import os
import sys
import re
import time
import urllib

from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

from statelegiscraper.assets.package import wa_committees

"""
#TESTING 

dir_chrome_webdriver = "/Users/katherinechang/Google Drive/My Drive/State Legislatures/StateLegiscraper/statelegiscraper/assets/chromedriver/chromedriver_v96_m1"

param_committee = "Senate Early Learning & K-12 Education"

wa_committees.senate_standing

param_year = "2015"

dir_save = "/Users/katherinechang/Google Drive/My Drive/State Legislatures/"
"""

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
            Standing committee hearing name.
            See available list through package assets
            "from statelegiscraper.assets.package import wa_names"
        param_year : String
            Calendar year (Current coverage limited to 2015-2021).
        dir_chrome_webdriver : String
            Local directory that contains the appropriate Chrome Webdriver.
        dir_save : String
            Local directory to save JSON with audio links.
    
        Returns
        -------
        A JSON file saved locally with selected committee and year audio links
    
        """
        
        if not isinstance(param_committee, str):
            raise ValueError("Committee name must be a string")
        else:
            pass

        if not isinstance(param_year, str):
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

        ############
        
        #--> DRIVER SETUP
        service = Service(dir_chrome_webdriver)
        options = webdriver.ChromeOptions()
        # Chrome runs headless, 
        # comment out "options.add_argument('headless')"
        # to see the action
        # options.add_argument('headless')
        driver = webdriver.Chrome(service=service, options=options)
        
        ############
        
        #--> OPEN TO TVW ARCHIVES 
        driver.get("https://tvw.org/video-search/")
        time.sleep(5)
        
        ############
        
        #--> CLICK CATEGORIES TO OPEN 
        driver.find_element(By.CLASS_NAME, "MuiGrid-grid-xs-12").click()
        
        # INPUT COMMITTEE NAME
        input_search = driver.find_element(By.XPATH, "//input[contains(@class, 'MuiInputBase-input MuiInput-input')]")
        input_search.send_keys(param_committee)
        
        #TEST NOTE: Need to check that this specific div class is clickable for each committee selection
        committee_script_list =["//div[@class='MuiListItemText-root jss3 jss4 MuiListItemText-multiline'",
                                " and @title='",
                                param_committee,
                                "']"]
        separator = ""     
        committee_script = separator.join(committee_script_list)
        
        # SELECT COMMITTEE NAME FROM DROP DOWN
        driver.find_element(By.XPATH, committee_script).click()
        
        # CHECK THAT COMMITTEE NAME FROM DROP DOWN IS SELECTED
        committee_name_assert = driver.find_element(By.XPATH, "//span[@class='MuiChip-label']").get_attribute("innerHTML")
        
        #Ensure amp is the same
        if re.search("&amp;", committee_name_assert):
            committee_name_assert = committee_name_assert.replace("&amp;", "&")
        else:
            pass
            
        assert committee_name_assert == param_committee, "Committee Name Not Selected"

        ############
        
        #--> SELECT START DATE BY LEGISLATIVE SESSION (JANUARY 1-3, WHICHEVER FALLS ON WEEKDAY)
        # Date is reliant on current date, start month set to January 1st of cal year
        calendar_dropdown = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__input-container']")        

        calendar_dropdown[0].click() 
        
        date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        start_date = date_elements[0].get_attribute("value")
        start_datetime = datetime.strptime(start_date, '%m/%d/%Y').date()
        
        previous_month_click = "//button[@class='react-datepicker__navigation react-datepicker__navigation--previous']"
       
        def _loop_january(driver, upper_range: int) -> ():
            if upper_range == 0:
                return
            for i in range(0, upper_range):
                driver.find_element(By.XPATH, previous_month_click).click()

        def _loop_first():
            try:
                driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--001']").click() 
            except:
                try:
                    driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--002']").click()
                except:
                    try:
                        driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--003']").click()
                    except:
                        pass
     
        _loop_january(driver, start_datetime.month-1)
        _loop_first()
        
        try:
            driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").is_enabled()
            calendar_dropdown[0].click()  
        except NoSuchElementException:
            pass            
        
        param_dates = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        param_start_date = param_dates[0].get_attribute("value")        
        param_start_datetime = datetime.strptime(param_start_date, '%m/%d/%Y').date()
        assert (param_start_datetime.month == 1), "Start Date not set to January"
        assert (param_start_datetime.day <=3), "Start Date not set between January 1-3"
        
        #--> SELECT START YEAR (ESTABLISHED BY PARAM_YEAR)
        
        #check if dropdown is down
        
        try:
            calendar_dropdown[0].click() 
        except:
            calendar_dropdown = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__input-container']")   
            calendar_dropdown[0].click() 
        
        assert driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").is_enabled(), "Calendar dropdown not available"
        
        date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        year_date = date_elements[0].get_attribute("value")
        year_datetime = datetime.strptime(year_date, '%m/%d/%Y').date()   
        
        driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").click() 
        
        #Year dropdown is dynamic according to date, code clicks according to present values  
        check_yr = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")
        check_yr_values=[]
        
        for y in range(len(check_yr)):
            check_yr_values.append(check_yr[y].get_attribute("innerHTML"))
            
        #Click previous until year appears on year_list
        #if not param_year in year_list:
        while not param_year in check_yr_values:
            driver.find_element(By.XPATH, "//a[@class='react-datepicker__navigation react-datepicker__navigation--years react-datepicker__navigation--years-previous']").click()
            while_year = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")
            while_year_values=[]
            for y in range(len(while_year)):
                while_year_values.append(while_year[y].get_attribute("innerHTML"))
            if param_year in while_year_values:
                break
            
        year_list = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")
        year_list_values=[]
        
        for y in range(len(year_list)):
            year_list_values.append(year_list[y].get_attribute("innerHTML"))
            
        assert param_year in year_list_values, "param_year not in year dropdown list"
            
        def _year_select(param_year):
            #Click according to the param_year
            if param_year == "2021":
                param_y = year_list_values.index("2021")
                year_list[param_y].click()
            elif param_year == "2020":
                param_y = year_list_values.index("2020")
                year_list[param_y].click()
            elif param_year == "2019":
                param_y = year_list_values.index("2019")
                year_list[param_y].click()
            elif param_year == "2018":
                param_y = year_list_values.index("2018")
                year_list[param_y].click()
            elif param_year == "2017":
                param_y = year_list_values.index("2017")
                year_list[param_y].click()
            elif param_year == "2016":
                param_y = year_list_values.index("2016")
                year_list[param_y].click()
            elif param_year == "2015":
                param_y = year_list_values.index("2015")
                year_list[param_y].click()
            else:
                "Invalid Year. Current coverage limited to 2015 to 2021"
                
        if (year_datetime.year != int(param_year)):
            _year_select(param_year)
            _loop_first()
        else:
            pass
        
        param_dates = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        param_start_date = param_dates[0].get_attribute("value")        
        param_start_datetime = datetime.strptime(param_start_date, '%m/%d/%Y').date()
        assert (param_start_datetime.year == int(param_year)), "Start Date not set to param_year"
        assert (param_start_datetime.day <=3), "Start Date not set between January 1-3"
        time.sleep(2)
        
        ############
        
        #--> SELECT END DATE BY LEGISLATIVE SESSION (DECEMBER)
        
        calendar_dropdown[1].click() 
        date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        end_date = date_elements[1].get_attribute("value")        
        end_datetime = datetime.strptime(end_date, '%m/%d/%Y').date()
        
        next_month_click = "//button[@class='react-datepicker__navigation react-datepicker__navigation--next']"
      
        def _loop_december(driver, upper_range: int) -> ():
            if upper_range == 12:
                 return
            for i in range(0, (12-upper_range)):
                driver.find_element(By.XPATH, next_month_click).click()
                
        def _loop_end():
            try:
                driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--031']").click() 
            except:
                try:
                    driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--030']").click()
                except:
                    try:
                        driver.find_element(By.XPATH, "//div[@class='react-datepicker__day react-datepicker__day--029']").click()
                    except:
                        pass
   
        _loop_december(driver, end_datetime.month)
        _loop_end()

        try:
            driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").is_enabled()
            calendar_dropdown[0].click()  
        except NoSuchElementException:
            pass  
        
        param_dates = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        param_end_date = param_dates[1].get_attribute("value")        
        param_end_datetime = datetime.strptime(param_end_date, '%m/%d/%Y').date()
        assert (param_end_datetime.month == int(12)), "End Date not set to December"
        assert (param_end_datetime.day >=29), "End Date not set between December 29-31"
        
        #--> SELECT END YEAR (ESTABLISHED BY PARAM_YEAR)
        
        try:
            calendar_dropdown[1].click() 
        except:
            calendar_dropdown = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__input-container']")   
            calendar_dropdown[1].click() 
            
        assert driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").is_enabled(), "Calendar dropdown not available"
        
        date_elements = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        end_year_date = date_elements[1].get_attribute("value")
        end_year_datetime = datetime.strptime(year_date, '%m/%d/%Y').date()   
        
        driver.find_element(By.XPATH, "//div[@class='react-datepicker__header']").click() 
        
        #Year dropdown is dynamic according to date, code clicks according to present values  
        check_yr = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")
        check_yr_values=[]
        
        for y in range(len(check_yr)):
            check_yr_values.append(check_yr[y].get_attribute("innerHTML"))
            
        #Click previous until year appears on year_list
        while not param_year in check_yr_values:
            driver.find_element(By.XPATH, "//a[@class='react-datepicker__navigation react-datepicker__navigation--years react-datepicker__navigation--years-previous']").click()
            while_year = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")
            while_year_values=[]
            for y in range(len(while_year)):
                while_year_values.append(while_year[y].get_attribute("innerHTML"))
            if param_year in while_year_values:
                break
            
        year_list = driver.find_elements(By.XPATH, "//div[@class='react-datepicker__year-option']")
        year_list_values=[]
        
        for y in range(len(year_list)):
            year_list_values.append(year_list[y].get_attribute("innerHTML"))
            
        assert param_year in year_list_values, "param_year not in year dropdown list"
        
        if (end_year_datetime.year != int(param_year)):
             _year_select(param_year)
             _loop_end()
        else:
             calendar_dropdown[1].click()
        
        param_dates = driver.find_elements(By.XPATH, "//input[@class='css-13hc3dd']")
        param_end_date = param_dates[1].get_attribute("value")        
        param_end_datetime = datetime.strptime(param_end_date, '%m/%d/%Y').date()
        assert (param_end_datetime.year == int(param_year)), "End Date not set to param_year"
        assert (param_end_datetime.day >=29), "End Date not set between December 29-31"

        ############
             
        #--> PRESS SUBMIT 
        driver.find_element(By.XPATH, "//button[@class='filter__form-submit css-1l4j2co']").click()
         
        ############
         
        # SAVE HTML FOR MULTIPLE PAGES
 
        url_html = []
        url_html.append(driver.page_source) #CURRENT PAGE, PAGE 1
        
        soup_html_home = BeautifulSoup(url_html[0])
        
        no_results_assert=soup_html_home.find('div', {'class': re.compile(r'fallback-states__NoResults.*')})
        
        if no_results_assert is None: #There are results
            pass
        else: #There are no results
            if no_results_assert.text == str("No Events Available"): #Check if there's the string
                url_html=["No results found"]
                print("Search results yielded no hearing meetings")
                #driver.close() #If no results breaks script, but otherwise run
                #break #Probably need to print why break so user knows what's up
            else:
                pass
            
        page_num = soup_html_home.find_all('button', {'class': re.compile(r'pagination__Button-.*')})
        
        if page_num==[]:
            pass
        else:
            for s in range(len(page_num)):
                for span_tag in page_num[s].findAll('span'): 
                    #better to find button tag, this finds span and deletes
                    span_tag.replace_with('')
            
            page_button_tag=[]
        
            for b in range(len(page_num)):
                page_tag = re.findall((r'(?<=<button class=").*?(?=" type="button"></button>)'), str(page_num[b]))
                page_button_tag.append(page_tag)
                
            page_button_tag_dup = [i[0] for i in page_button_tag]
            
            page_button_tag = list(OrderedDict.fromkeys(page_button_tag_dup))
                    
            if len(page_button_tag) > 1:
                for p in range(len(page_button_tag)-1):
                    print(p+1)
                    button_script_list = ["//button[@class='",
                                          page_button_tag[p+1],
                                          "']"]
                    separator = ""     
                    button_script = separator.join(button_script_list)
                    time.sleep(5)
                    button_click = driver.find_element(By.XPATH, button_script)
                    driver.execute_script("arguments[0].click();", button_click)
                    time.sleep(5)
                    url_html.append(driver.page_source)
                    home_click = driver.find_element(By.XPATH, "//button[@class='filter__form-submit css-1l4j2co']")
                    driver.execute_script("arguments[0].click();", home_click)
                    """
                    try:
                        home_script_list = ["//button[@class='",
                                              page_button_tag[0],
                                              "']"]
                        separator = ""     
                        home_script = separator.join(button_script_list)
                        time.sleep(5)
                        driver.find_element(By.XPATH, home_script).click()
                    except:
                        driver.find_element(By.XPATH, "//button[@class='filter__form-submit css-1l4j2co']").click()
                    """
                    
        assert len(url_html) > 0, "Check that there's content in the html list"
        
        driver.close()
        
        #If there are no results, need to identify and break before moving next
        #Check other pages beyond first in url_html to identify if there are no events available
        #If so, then delete the identified element with "No Events Available" on that page
        
        ####
        
        # FOR EACH PAGE SOURCE SEARCH FOR A HREF TAG ENDING IN .MP3 TO CREATE A LIST OF AUDIO LINKS, 
        
        committee_html={}
        k=0

        for url_page in range(len(url_html)):
            soup_html = BeautifulSoup(url_html[url_page])
            table = soup_html.find_all('div', {'class': re.compile(r'table__Metadata-.*')})
            for t in range(len(table)):
                committee_html[k]=(table[t])
                k+=1
                
        #TBD: Delete any entries that aren't the same committee name as the rest
        #Search to make sure committee name matches
        
        #Extract datetime format and set as key
        #and then mp3
        committee_datetime=[]
        committee_audio_link=[]
        for key in range(len(committee_html)):
        
            key_datetime=committee_html[key].get_text(separator="____")
            key_datetime_found = re.findall(r'(\d+/\d+/\d+)',key_datetime)
            
            key_datetime_found[0]
            
            committee_datetime_found =  datetime.strptime(key_datetime_found[0], '%m/%d/%Y').date()
            committee_datetime.append(str(committee_datetime_found)) #Should keep as datetime? Currently string

            links_all = committee_html[key].findAll('a', href=True)
            links_mp3 = [l for l in links_all if l['href'].endswith('.mp3')]
            
            for l in links_mp3: 
                committee_audio_link.append(l['href'])
                
        assert len(committee_datetime)==len(committee_audio_link), \
            "Dates and audio links aren't the same size"
        
        committee_date_links={}
        
        if len(committee_datetime)==len(committee_audio_link):
            committee_date_links = dict(zip(committee_datetime, committee_audio_link))
        else:
            raise IndexError("Dictionary keys and values don't match")
        
        # SAVE committee_links AS JSON LOCALLY TO DIR_SAVE
        
        committee_name = re.sub(r'[^A-Za-z0-9 ]+', '', param_committee)
        
        committee_name = committee_name.strip().replace(" ", "")
        
        final_file = ("wa_" + str(committee_name.lower()) + "_" + str(param_year)+ ".json")
        
        final_dir_file = os.path.join(dir_save, final_file)
        
        with open(final_dir_file, 'w') as final:
            json.dump(committee_date_links, final, sort_keys=True, indent=4)
            
    
    def wa_scrape_audio(audio_json, dir_audio_save):
        """

        Parameters
        ----------
        audio_json : JSON
            JSON file name, include full local path.
        dir_audio_save : String
            Local directory to download audio files in.
            Best if the directory is empty

        Returns
        -------
        Audio files linked in audio_json.

        """
        
        file_path = open(audio_json,)
        audio_links = json.load(file_path)
        
        import urllib
        
        loop_url = str(list(audio_links.values())[0])
        loop_file_name = str(list(audio_links)[0]) + ".mp3"
        loop_file_dir = os.path.join(dir_audio_save, loop_file_name)
        
        urllib.request.urlretrieve(req, loop_file_dir)
        
            
        
        
audio_json="/Volumes/GoogleDrive/My Drive/State Legislatures/wa_houseeducation_2015.json"

dir_audio_save="/Volumes/GoogleDrive/My Drive/State Legislatures/tests/"

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
        

