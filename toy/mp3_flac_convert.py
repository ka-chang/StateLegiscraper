#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
K Note: Need to convert mp3 to flac to run in Google Speech-to-Text API for technology review
comparison with Deep Speech.

Run with python3 mp3_flac_convert.py in CL to convert
"""

import os
from pydub import AudioSegment

os.chdir("/Volumes/GoogleDrive/My Drive/2021/Fall 2021/CSE583/project/leg-text-scraper/") #Set to Github folder,

toy_org = "toy/wa_senate_bfst_2021_0119.mp3"
toy_flac = "toy/outputs/wa_senate_bfst_2021_0119.flac"

sound = AudioSegment.from_mp3(toy_org)
sound.export(toy_flac, format="flac")
