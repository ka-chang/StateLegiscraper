# -*- coding: utf-8 -*-

import json

file = open("/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/leg-text-scraper/toy/data_txt/wa_senate_bfst_2021_0119.json",)

data = json.load(file)
data_trim = data["results"]
transcript=""

for num in range(len(data_trim)):
    transcript+=str(data_trim[num]["alternatives"][0]["transcript"])

transcript_txt = open('/Users/katherinechang/Google Drive/My Drive/2021/Fall 2021/CSE583/project/leg-text-scraper/toy/data_txt/wa_senate_bfst_2021_0119_GOOG.txt', 'w')
transcript_txt.write(transcript)
transcript_txt.close()
