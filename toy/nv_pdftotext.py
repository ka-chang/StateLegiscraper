# -*- coding: utf-8 -*-
"""
Extract text from pdf
"""
import os
import requests
import pdfplumber
import string
import json

directory=r'/Users/' #NEED DIRECTORY
n=0
nram = {} #nram is just one committee. We will need to modularize this so it can be adjusted for all committees

file_list = os.listdir(directory)
file_list.sort()
del file_list[0]

for file in file_list:
    filename = directory + file
    all_text = '' # new line
    with pdfplumber.open(filename) as pdf:
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text()
            #print( single_page_text )
            # separate each page's text with newline
            all_text = all_text + '\n' + single_page_text
            nram[n]=all_text
    n=n+1   
            # print(text) - comment out or remove line  
            
with open('nv_leg_nram.json', 'w') as f:
    json.dump(nram, f, ensure_ascii=False)



