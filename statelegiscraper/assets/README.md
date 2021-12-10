# Assets

The included files are assets that StateLegiscraper uses to conduct webscraping and to transcribe audio files to text. Many of the necessary files are provided here to keep StateLegiscraper self-contained and to assist with ease of use. 

## Requirements

### Chrome Driver

As an option, users can save the appropriate Chrome Driver file in the assets folder. Please see [these instructions](https://github.com/ka-chang/StateLegiscraper#google-chrome-and-chrome-driver) for more details.

### DeepSpeech

DeepSpeech requires three separate assets to run: DeepSpeech Examples VAD Transcribe, DeepSpeech Model, v.0.9.3, and DeepSpeech Model Scorer, v.0.9.3.

[DeepSpeech Examples VAD Transcribe](https://github.com/mozilla/DeepSpeech-examples) files are included in this assets directory, but users will need to directly download the Model and Model Scorer files. Their large file size preclude hosting them on our Github repository. You can download the files manually by right clicking the links below, or navigating to this folder through your terminal and running the following scripts. Make sure to retain the file names and to save them in the `statelegiscraper/assets` folder.

`curl -o https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm`

`curl -o https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer`

Required DeepSpeech Model Source Links:

- [DeepSpeech Model, v.0.9.3](https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.pbmm)
- [DeepSpeech Model Scorer, v.0.9.3](https://github.com/mozilla/DeepSpeech/releases/download/v0.9.3/deepspeech-0.9.3-models.scorer)

All copyright and license notices are preserved per [DeepSpeech's license](https://github.com/mozilla/DeepSpeech/blob/master/LICENSE).
