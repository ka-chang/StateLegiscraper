"""
CA module for scraping and processing text from http://www.legislature.ca.gov/ 

# Status

Current Coverage (In Design Phase, see Notes):
    [ ] Committee Hearings (Audio Links): Assembly (2018 - 2021)
    [ ] Committee Hearings (Audio Links): Senate (2005 - 2021)

Planned Coverage:
    [ ] Floor Speeches 

# CA Work Flow

StateLegiscraper has two classes for each state module:

    CAScrape includes 2 functions 

    CAProcess includes 2 functions that processes raw data

CLASS CAScrape
    - ca_scrape_weblinks
    - ca_scrape_audio

CLASS CAProcess
    - ca_speech_to_text
    - ca_text_clean

# Notes

Assembly archive at https://www.assembly.ca.gov/media-archive
Archive only from 2018-2021 (might want to collect this data , process into text, and host on GH?)
Input search term and results provide the date, title, and a video and audio link.
Do a check to ensure the name of the row matches a standing committee (there are lots of select)

Senate archive at https://www.senate.ca.gov/media-archive
Archive from 2005 - 2021, uses same search and page set-up as Assembly media archive

"""


