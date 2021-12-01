# LegTextScraper

A text webscraping tool for U.S. state legislature websites, with options for speech-to-text generated transcripts and public-facing example dashboards that include basic text analysis on specific policy areas.

## Mission

The mission of LegTextScraper is to build and make accessible text corpora of political, social, and scholarly significance that can build greater public transparency and academic knowledge about public policymaking and state-level politics. 

## Project Objective

In recent years, a number of controversial bills and policy proposals have emerged in state legislatures and media attention has increasingly focus on state legislative politics. But beyond recent news, public oversight of the policymaking process is an important cornerstone of democratic nations. As the current U.S. political climate has increasingly shifted national politics to the state-level, state legislatures are key policy venues to watch.

However, unlike the U.S. Congress, the 50 state legislatures have vastly different websites and public documentation protocols. Therefore, a systemic examination of national trends at the state-level is difficult to execute due to challenges in navigating, accessing, and processing relevant data. While projects such as [Civic Eagle](https://www.civiceagle.com/) and [Open States](https://openstates.org/) have APIs that provide data for bills and representatives across all 50 states, there is currently no open source option that scrapes and processes committee hearing written and spoken transcripts for research purposes and public review. 

## Requirements

## Installation

## Usage

### Tool

LegTextScraper contains U.S. state-specific modules that each contain two classes of functions: a Scrape class and a Process class. 

- The Scrape class bundles functions that scrape U.S. state legislature websites for individual committee hearing and floor speech PDF / audio / video transcript links. Users export this raw data to their local drive or a mounted cloud drive.
- The Process class bundles functions that cleans and formats the raw scraped data into Python objects appropriate to use for popular NLP packages (e.g., nltk, SpaCy). Scraped PDF files will be converted to dictionary objects, while audio and video files will use Deep Speech, an open-source speech-to-text engine, to generate a text transcript of selected meetings. These transcripts can be used as dictionary objects, or exported as a JSON file.

### Dashboard

LegTextScraper also includes a series of public-facing dashboards using the scraped state legislature data. These dashboards  provide interested users about high-level narrative trends within a specific state and/or policy area. 

- COVID-19 Narrative Trends in Nevada's Health and Human Services Committee (2020) 

## Use Cases

Researchers can gather raw data for nuanced, tailored analysis, while journalists and members of the public can engage with our text analysis dashboards to capture high-level trends in the political discourse at the state legislature.

## Requests 
The ambition of LegTextScraper is to one day cover and maintain all 50 state legislature websites. If you'd like to request a state, build a dashboard, or suggest a feature to extend the functionality of LegTextScraper, please feel free to [raise an issue](https://github.com/ka-chang/LegTextScraper/issues). 

## Bug Report
If you would like to report a bug or issue , please submit a detailed report at [this link](https://github.com/ka-chang/LegTextScraper/issues/new).
 
## Contributions
If you'd like to expand LegTextScraper to other states, use the data to add to our dashboard options, or add additional features to the tool, please fork the repository, add your contribution, and generate a pull request. The complete contributing guide can be found at this [link](https://github.com/ka-chang/LegTextScraper/blob/main/doc/CONTRIBUTING.md).

## Acknowledgements
Many thanks to Dr. David Beck and Anant Mittal from the University of Washington for their support, guidance, and feedback in the development of this package.
