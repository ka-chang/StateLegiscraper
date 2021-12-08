# StateLegiscraper Design Specification

## Description

The goal of the project is to build a public facing webscrapper tool that makes text transcripts of state legislature committee 
hearing readily available to researchers and members of the public.  In particular, this project has two parts. 

1. Build a tool to scrape all available text transcripts of committee hearing and prepares its for text analytics. This 
tool is to publicly available for users to gather raw data. If text transcripts are not available, as often the case for state legislature websites, we scrape the available audio and convert it to text using [DeepSpeech](https://deepspeech.readthedocs.io/en/r0.9/), an open-source speech-to-text engine.

2. Build a dashboard of text analytics to indicate the power of this text corpora, with a focus on 
word frequency, sentiment analysis, and topic modeling of specific committee hearings (that is, policy area across time) and/or for specific sessions 
(that is, what’s the most salient topic discussed during a legislative session). We utilize [nltk](http://ntlk.org), Natural Language Tool Kit, for analysis.

## Background

As many members of public may have seen on the news, recent media attention has focused on state legislative politics and a 
number of controversial bills and policy proposals that have emerged in the past few years. But beyond recent news, public 
oversight of the policymaking process is an important cornerstone of democratic nations. As the current U.S. political climate 
has increasingly shifted national politics to the state-level, state legislatures are key policy venues to watch.

However, unlike the U.S. Congress, the 50 state legislatures have vastly different websites and public documentation protocols. 
Therefore, a systemic examination of national trends at the state-level is difficult to execute due to challenges in navigating and 
accessing data. While projects such as [Civic Eagle](https://www.civiceagle.com) and [Open States](https://openstates.org) have APIs that provide data for bills and representatives across all 50 states, there is currently no open source option that scrapes transcripts of committee hearings for research purposes and public review.

## User Profile and Use Cases

The use case of this tool is to build and make accessible text corpora of political, social, and scholarly significance that can build greater public transparency about public policymaking and state-level politics. Researchers would be interested in this tool to gather raw data for nuanced, tailored analysis, while journalists and members of the public can engage with our text analysis dashboard to capture high-level trends in the political discourse at the state legislature.

- *Researchers*: Researcher are the people who analyze the raw transcripts data of committee videos to induce some useful information. The scrapper should allow researchers to use our interactive dashboard to select the state, committee, and date and download the raw audio files for that selection. Additionally, researchers can also obtain speech-to-text transcripts of the raw data selected. 

- *Members of the Public*: Members of the public want to directly capture high-level political information from the dashboard. The dashboard needs to provide well-processed data and analysis from selectedstate legislatures. There would be two buttons for Washington state and Nevada state that journalists can select from. Under each state, there would be several concerning topics (eg. COVID-19, Long-term Care Act etc.) and if journalists are interested in one of them, he/she can enter to see the analysis(visualizations) about this topic.

## Components
![alt text](https://github.com/ka-chang/leg-text-scraper/blob/main/doc/Flow%20chart.PNG)

**Component 1. State, Chamber, Committee, and Date (Audio)** 

- *Inputs*: Radio buttons for users to select state of interest (of those available, currently Washington), chamber (state-specific equivalent of House and Senate), Committee (complete list), and Date (organized by legislative session year and limited by those available on the website).
- *Outputs*: User can choose to download the raw audio files for the entire legislative session, or a single JSON file generated from speech-to-text function

**Component 2. State, Chamber, Committee, and Date (PDF)** 
- *Inputs*: Radio buttons for users to select state of interest (of those available, currently Nevada), chamber (state-specific equivalent of House and Senate), Committee (complete list), and Date (organized by legislative session year and limited by those available on the website).
- *Outputs*: User can choose to download the raw PDF files for the entire legislative session, or a single JSON file generated from PDF to text function

**Component 3. Text Analytics Topic Selection**
- *Inputs*:  Drop down menu for users to select a team-determined topic of choice and state of interest. For Fall 2021, the dashboard will focus on COVID-19 and Nevada state data.
- *Outputs*: An updated dashboard of text analytics visualizations on the topic selected for the state. Analysis categories include: word frequency and counts, sentiment analysis, IDF, and unsupervised topic model categories.

## Interactions

## Project Plan

| Class Dates 	| Deliverable/Milestone 	| Project Task 	| WA Task 	| NV Task 	|
|---	|---	|---	|---	|---	|
| Nov 2/4 	| Software Design (Nov 2) 	| - Start scraping code for WA/NV<br>- Complete design_spec.md 	| - Play with WA toy audio files <br>- Implement with DeepSpeech<br>- Generate one transcript with DeepSpeech<br>- Generate one transcript with Google API 	| - Play with NV pdf files<br>- Convert PDF to json<<br>- Conduct a word count of toy files 	|
| Nov 9/11 	|  	| - Speak to Anant about file management<br>- Prepare technology review slide deck<br>- Write unit tests for web scrapping WA/NV 	| - Scrape audio files for one session<br>- Generate transcripts for one session 	| - Scrape all pdfs, convert PDF to json<br>- Conduct sentiment analysis<br> 	|
| Nov 16/18 	| Technology Review (Nov 16) 	|  	| - Scrape audio files for all sessions<br>- Generate transcripts for all sessions 	| - Conduct unsupervised topic modeling 	|
| Nov 23/25 	|  	| - Build front end for data collection (NV/WA)<br>-  	| - Build simple dashboard of word count 	| - Build dashboard 	|
| Nov 30/Dec 2 	|  	| -Sync up WA and NV efforts 	| - Sync up WA data with NV dashboard code 	| - Dashboard running for team to review 	|
| Dec 7/Dec 9 	| Project Previews  	|  	|  	|  	|
