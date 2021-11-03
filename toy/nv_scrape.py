#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  1 17:52:23 2021

@author: katherinechang
"""
"""
#<div id="divCommitteePageMeetings" aria-labelledby="tabMeetings" role="tabpanel" class="k-content k-state-active" aria-expanded="true" style="display: block;">
#<div id="divMeetings" class="content" data-selected-meeting-key>
#<div id="committee-meetings-tab">
#Actual commitee items under <div id="divMeetings">
#Minutes download button on <a class="btn btn-outline-dark" href=... title="View the minutes for this meeting">


"""

import os
import requests
import re
import time
import urllib.request
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from selenium import webdriver

ed_links=[
    "https://www.leg.state.nv.us/App/NELIS/REL/80th2019/Committee/228/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/80th2019/Committee/216/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/79th2017/Committee/168/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/79th2017/Committee/185/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/78th2015/Committee/50/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/78th2015/Committee/66/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/77th2013/Committee/2/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/77th2013/Committee/13/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/76th2011/Committee/25/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/76th2011/Committee/36/Meetings"
]

nram_links=[
    "https://www.leg.state.nv.us/App/NELIS/REL/80th2019/Committee/225/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/80th2019/Committee/235/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/79th2017/Committee/186/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/79th2017/Committee/174/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/78th2015/Committee/67/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/78th2015/Committee/56/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/77th2013/Committee/16/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/77th2013/Committee/7/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/76th2011/Committee/39/Meetings",
    "https://www.leg.state.nv.us/App/NELIS/REL/76th2011/Committee/30/Meetings"
]

for link_index in range(len(nram_links)):
    driver=webdriver.Chrome("/Users/katherinechang/Documents/PhD/UW/2021 Spring/POLS 559/project_stateleg/chromedriver")
    time.sleep(20)
    driver.get(nram_links[link_index]) #change to nram_link[] or ed_link[]
    time.sleep(20)

    arrow01 = driver.find_element_by_id('divCommitteePageMeetings')
    arrow01.click()
    time.sleep(10)
    
    arrow02 = driver.find_element_by_id('divMeetings')
    arrow02.click()
    
    #arrow03 = driver.find_element_by_id('committee-meetings-tab')
    #arrow03.click()
    
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
    
    #If there is no such folder, the script will create one automatically
    folder_location = r'/Users/katherinechang/Documents/PhD/UW/2021 Spring/POLS 559/project_stateleg/nram'
    #if not os.path.exists(folder_location):os.mkdir(folder_location)
    
    for link in all_files:
        filename = os.path.join(folder_location,"_".join(link.split('/')[4:]))
        urllib.request.urlretrieve(link, filename)
    time.sleep(45)
        
    driver.close()
        
