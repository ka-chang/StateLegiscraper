# <img src= "doc/images/statelegiscraper_logo.png" height="60"></img> StateLegiscraper 

<img src="doc/images/readme_map/readme_map.png" height="200" width="350" align=right></img>

A webscraping tool for U.S. state legislature websites that exports and processes standing committee hearing transcript data for text analysis.

## Mission

The mission of StateLegiscraper is to make accessible text corpora of political, social, and scholarly significance that can build greater public transparency and academic knowledge about public policymaking and state-level politics. 

## Project Objective

In recent years, a number of controversial bills and policy proposals have emerged in state legislatures and media attention has increasingly focused on state legislative politics. But beyond recent news, public oversight of the policymaking process is an important cornerstone of democratic nations. As the current U.S. political climate has increasingly shifted national politics to the state-level, state legislatures are key policy venues to watch.

However, each of the 50 state legislatures have vastly different websites and public documentation protocols. Standing committee hearings in each state are archived in a variety of formats (e.g., PDF, audio, or video), making it difficult to access data, at scale, about the work that happens during the hearing process. Committee hearings are rich sources of data that captures crucial elements of the policy process, such as interactions between policy actors, strategic use of policy narratives, issue framing, just to name a few. 

However, a systemic examination of within state and national trends of state legislature committee hearings is difficult to execute due to challenges in navigating, accessing, and processing relevant data at scale and across time. While projects such as [LegiScan](https://legiscan.com), [Civic Eagle](https://www.civiceagle.com/), and [Open States](https://openstates.org/) have APIs that provide data about bills and representatives across all 50 states, there is currently no open source option that scrapes and processes written and spoken transcripts of state legislature commitee hearings and floor speeches for research purposes and public review. StateLegiscraper is an open-source tool that fills this data access gap by making all publically available state legislature committee hearing data easily accessible regardless of its archived format. 

## Repository Structure
 ```
.
├── data
│   └── dashboard
├── doc
├── examples
├── statelegiscraper
│   ├── assets
│   ├── helpers
│   ├── states
│   └── test
├── LICENSE
├── README.md
└── environment.yml
 ```
The `statelegiscraper` directory includes a `states` module, unit tests in `test`, and a `helpers` module that adds closed-source speech-to-text functionality with [Google Cloud](https://cloud.google.com/speech-to-text). Data relevant to dashboard are included in `data` directory. The `examples` directory provides example Jupyter notebooks that can help new users learn the ways StateLegiscraper organize scraping and processing. 

## Installation

StateLegiscraper is installed using the command line and is best used with a virtual environment due to its dependencies.

1. Open your choice of terminal (e.g., Terminal (MacOS) or [Ubuntu 20.04 LTS](https://www.microsoft.com/en-us/p/ubuntu-2004-lts/9n6svws3rx71?activetab=pivot:overviewtab) (Windows))
2. Clone the repoistory using `git clone https://github.com/ka-chang/StateLegiscraper.git`
3. Change to the StateLegiscraper directory using `cd StateLegiscraper`
4. Set up a new virtual environment with all necessary packages and their dependencies using `conda env create -f environment.yml`
5. Activate the statelegiscraper virtual environment with `conda activate statelegiscraper`
6. Deactivate the statelegiscraper virtual environment using `conda deactivate`

## Requirements

### Google Chrome and Chrome Driver

StateLegiscraper's webscraping tool uses a Python-based web browser automation tool, [Selenium](https://www.selenium.dev). This requires a specific browser and browser driver to work properly. The package is built using Google Chrome.

- [Google Chrome](https://www.google.com/chrome/)  
- [Chrome Driver](https://chromedriver.chromium.org/downloads)

To check your installed Chrome version and to download the appropriate Chrome Driver, follow these instructions:
1. Open Google Chrome
2. At the top right corner of the browser, click the settings tab (three vertical dots ⋮)
3. Navigate down to Help > About Google Chrome
4. Your Google Chrome version is listed on the top of the page. For example:

<img src="doc/images/readme_chrome.png">

5. Find the [Chrome Driver](https://chromedriver.chromium.org/downloads) that corresponds to your version and save it to your local drive. We recommend saving it within the cloned repository directory `statelegiscraper/assets` for organizational purposes.

### DeepSpeech Model Files

StateLegiscraper uses an open-source speech-to-text engine called [DeepSpeech](https://github.com/mozilla/DeepSpeech/) to process audio files to text transcripts. DeepSpeech requires acoustic models to run, which StateLegiscraper's audio_to_text functions require. You can read more about DeepSpeech's acoustic models in their release notes [published here](https://github.com/mozilla/DeepSpeech/releases/tag/v0.9.3).

To download DeepSpeech's v.0.9.3 models and v.0.9.3 model scorer, follow these instructions in your terminal of choice:

1. Navigate the the assets folder in the statelegiscraper package using `cd statelegiscraper/assets`.
2. Download the DeepSpeech's v.0.9.3 models into the assets directory using `curl -o https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm`
3. Download the DeepSpeech's v.0.9.3 model scorer into the assets directory using `curl -o https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer`

## Usage

### Tool

StateLegiscraper contains U.S. state-specific modules that each contain two classes of functions: a Scrape class and a Process class. 

- The Scrape class bundles functions that scrape U.S. state legislature websites for individual committee hearing and floor speech PDF / audio / video transcript links. Users export this raw data to their local drive or a mounted cloud drive.
- The Process class bundles functions that cleans and formats the raw scraped data into Python objects appropriate to use for popular NLP packages (e.g., nltk, SpaCy). Scraped PDF files will be converted to dictionary objects, while audio and video files will use Deep Speech, an open-source speech-to-text engine, to generate a text transcript of selected meetings. These transcripts can be used as dictionary objects, or exported as a JSON file.

Example Jupyter notebooks are provided in the [examples directory](https://github.com/ka-chang/StateLegiscraper/tree/main/examples) that walk new users through StateLegiscraper's scrape and process functions, including expected behavior from Selenium and file management strategies.

### Dashboard

StateLegiscraper also includes a series of public-facing dashboards using the scraped state legislature data. These dashboards  provide interested users about high-level narrative trends within a specific state and/or policy area. 

## Use Cases

Researchers can gather raw data for nuanced, tailored analysis, while members of the public can engage with our text analysis dashboards to capture high-level trends in the political discourse at the state legislature. Read detailed [user stories here](https://github.com/ka-chang/StateLegiscraper/blob/main/doc/user_stories.md).

## Requests 

The ambition of StateLegiscraper is to one day cover and maintain all 50 state legislature websites. If you'd like to request a state, build a dashboard, or suggest a feature to extend the functionality of StateLegiscraper, please feel free to [raise an issue](https://github.com/ka-chang/StateLegiscraper/issues). 

## Bug Report

If you would like to report a bug or issue , please submit a detailed report at [this link](https://github.com/ka-chang/StateLegiscraper/issues/new).
 
## Contributions

If you'd like to expand StateLegiscraper to other states, use the data to add to our dashboard options, or add additional features to the tool, please fork the repository, add your contribution, and generate a pull request. The complete contributing guide can be found at this [link](https://github.com/ka-chang/StateLegiscraper/blob/main/doc/CONTRIBUTING.md). This project operates under the [Contributor Code of Conduct](https://www.contributor-covenant.org/version/1/0/0/code-of-conduct/).

## Acknowledgements

Many thanks to Dr. David Beck and Anant Mittal from the University of Washington for their support, guidance, and feedback in the development of this package.

StateLegiscraper logo adapted from [Icon8](https://icons8.com/icons/authors/zkUJRGwffdqs/wanicon/external-wanicon-lineal-wanicon) icons.
