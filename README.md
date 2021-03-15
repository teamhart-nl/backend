# backend

Install requirements with `pip install -r /path/to/requirements.txt`

## Running the application
### Development mode
For running the application in development mode
1. Set the environment variables `FLASK_ENV=development` and `FLASK_APP=app.py` (on Windows this is done by `set <varname>=<varvalue>`)
2. Set the PRODUCTION boolean in definitions.py to `False`
3. Run the app with `flask run`

### Production mode (not distribution)
For running the application in production mode
1. Set the environment variables `FLASK_ENV=production` and `FLASK_APP=app.py` (on Windows this is done by `set <varname>=<varvalue>`)
2. Set the PRODUCTION boolean in definitions.py to `TRUE`
3. Run the app with `flask run`

## Creating distribution
1. build the frontend with `npm run build`
2. Put the `index.html` just generated in the `templates` folder in the backend.
3. Put the rest of the generated frontend files in the `static` folder in the backend.
4. Change the links in the `index.html` referring to js/img/css files by adding the prefix `static/`
5. Change the `PRODUCTION` boolean in the `definitions.py` file to `True`.
6. (optional) Change the `debug` option in the `arduino_config.json`. 
7. Generate the distribution using the command `pyinstaller --add-data "resources;resources" --add-data "templates;templates" --add-data "static;static" --icon="static\favicon.ico" app.py`

# API Specification

### Phonemes
<details>
<summary>/phonemes</summary>

get the phonemes which can be send to the microcontroller

REQUEST:

    GET /api/v1/phonemes

EXAMPLE RESULT:

    {'phonemes' : ['K', 'AE', 'A']}

</details>

### Microcontroller
<details>
<summary>/microcontroller/status</summary>

//NOT IMPLEMENTED

REQUEST:

    GET /api/v1/microcontroller/status

RESULT:

    {metrics for status}

</details>

<details>
<summary>/microcontroller/stop</summary>

//NOT IMPLEMENTED
Stop all haptic activity on the microcontroller.

REQUEST:

    GET /api/v1/microcontroller/stop

RESULT:

    {succes or nah}

</details>

<details>
<summary>/microcontroller/phonemes</summary>

Send a phoneme to the microcontroller directly

REQUEST:

    POST /api/v1/microcontroller/phonemes

BODY

    {'phonemes': ['K', 'L']}

EXAMPLE CURL (windows)

    curl -H "Content-Type: application/json" -d "{ \"phonemes\": [\"K\", \"M\"] }" http://localhost:5000/api/v1/microcontroller/phonemes

RESULT:

    200 if OK

</details>

<details>
<summary>/microcontroller/words</summary>

Send a list of words to the arduino, returns the phoneme breakdown.

REQUEST:

    POST /api/v1/microcontroller/words

BODY

    {'words': ['Team', 'Treat']}

EXAMPLE CURL (windows)

    curl -H "Content-Type: application/json" -d "{ \"words\": [\"Team\", \"Treat\"] }" http://localhost:5000/api/v1/microcontroller/words

RESULT:

    {
        "words" : ["Team", "HART"],
        "decomposition" : [
        {
            "phonemes" : ["T", "IY", "M"]
        },

        {
            "phonemes" : ["T", "R", "IY", "T]
        },
    ]}, 
    200 if OK

</details>

<details>
<summary>/microcontroller/sentences</summary>

Send a list of sentences to the arduino, returns the translation and fires microcontroller.

REQUEST:

    POST /api/v1/microcontroller/sentences

BODY

    {'sentences': ['This is sentence one.', 'This is sentence two.'], 'language': 'language abbreviated string'}
The 'language abbreviated string' can be either
1. 'en' for English
2. 'nl' for Dutch
3. 'de' for German
4. 'fr' for French
5. 'ru' for Russian

RESULT:

    {
        "sentences" : ["This is sentence one", "This is sentence two"],
        "translation" : ["Translation of sentence one", "Translation of sentence two"]
    }, 
    200 if OK

</details>

<details>
<summary>/microcontroller/audiopath</summary>

Send an audiopath of a file, fires microcontroller, and return transcription and translation.

REQUEST:

    POST /api/v1/microcontroller/audiopath

BODY

    {
        'path': 'C:\Users\user\Documents\file.flac'
        'source_language' : 'nl'
        'target_language' : 'en'
    }

EXAMPLE CURL (windows)

    curl -H "Content-Type: application/json" -d "{ \"path\": \"C:\\Projects\\tryout\\sound1channel.flac\", \"source_language\": \"nl\", \"target_language\": \"en\" }" http://localhost:5000/api/v1/microcontroller/audiopath

RESULT:

    {
        "transcription" : ["This is sentence one", "This is sentence two"],
        "translation" : ["Translation of sentence one", "Translation of sentence two"]
    }, 
    200 if OK

</details>

<details>
<summary>/microcontroller/audiofile</summary>

Send an audiofile,fires microcontroller, and return transcription and translation. This request is a bit different, as it is not a json post, but a multipart form. This multipart form contains two fields, one which is the audiofile in bytes, the second one which is the parameters in a json dumped to string. See the curl / body.

REQUEST:

    POST /api/v1/microcontroller/audiofile

BODY

    <form action="/microcontroller/audiofile" method="post" enctype="multipart/form-data">
    File: <input type="file" name="file"><br>
    Data: <input type="text" name="data"><br>
    <input type="submit" value="Submit">
    </form>

EXAMPLE PYTHON REQUEST (cus curl would be a bitch for this one)

    file = open(FILE_PATH, "rb")
	data = {"source_language": "nl", "target_language": "en"}
    # package stuff to send and perform POST request
	values = {"file": (FILE_PATH, file, "audio/flac"),
			"data" : ('data', json.dumps(data), 'application/json')}
	
	response = requests.post(URL, files=values)

RESULT:

    {
        "transcription" : ["This is sentence one", "This is sentence two"],
        "translation" : ["Translation of sentence one", "Translation of sentence two"]
    }, 
    200 if OK


</details>

# Events

## Overview of Events
<details>
<summary>GoogleTranscribeFileEvent</summary>
Transforms a local audio file into text written in given source language.

- Expects: 
    - _path_ which is a string filepath to the audio file
    - *audio_type* type of audio file
    - *spoken_language* 
- Modifies:
- Creates: _sentences_ result of the transcription: consecutive audio portions transcribed into sentences
    - currently in [SpeechRecognitionResult format](https://cloud.google.com/speech-to-text/docs/reference/rest/v1/speech/recognize#speechrecognitionresult): 

</details>

<details>
<summary>GoogleTranslateEvent</summary>

- Expects: 
    - *original_sentences*: list of lists with original strings
    - *source_language*
    - *target_language*
- Modifies:
- Creates: *translated_sentences* , list of [raw response bodies of the translate api](https://cloud.google.com/translate/docs/reference/rest/v2/translate#response-body)

</details>

<details>
<summary>PhonemeDecompositionEvent</summary>
Transforms an English sentence into phonemes

- Expects: _words_, which is an ordered list of strings representing the sentence, each string being a word.
- Modifies:
- Creates: _phonemes_, List of phonemes for each possibility of a word, for each word in the sentence (_words_)

</details>

<details>
<summary>SendPhonemesToArduinoEvent</summary>

Event that sends given phonemes to arduino

- Expects: 
    - _phonemes_, 3 dimensional list of strings: list of words, with every word being a list of decomposition, with each decomposition being list of phoneme-strings.
    - *phoneme_patterns* dictionary with (phoneme : json pattern) combinations
- Creates: 
    - *sent_phonemes*, list 

</details>

## Overview of Main Event Flow

request_data attributes that the events expect/modify/create, and their specification
- **sentences**: [ [ str ] ] 
- **phoneme_patterns**: Dict[str : JSON] dictionary with  available (phoneme : json pattern) combinations
- **phonemes**: [ [ [ [ str ] ] ] ] list of sentences, which are lists of words, with every word being a list of decomposition, with each decomposition being list of phoneme-strings. _created by PhonemeDecompositionEvent_
- **sent_phonemes**:  [ [ str ] ] the decompositions that were sent to the arduino, _created by SendPhonemesToArduinoEvent_

## Making Event Chains

How to trigger a series of events? This backend works with data-centric paradigm. In the background, different events are triggered based on what request data the **Dispatcher** (singleton) receives. The requestdata inherits from AbstractData and has an **EventType** (enum). That EventType has one or more affiliated Events (inheriting from AbstractEvent). Every event implements the static method *get_compatible_events()*, which returns in what EventTypes this belongs. In a way, you can understand EventType as "tags", where all events that have that tag belong to a certain event chain. So how does the dispatcher know in what order to handle the events? Every event stores a different integer attribute, the PRIORITY. Higher priorities get handled first. Each event modifies and/or reads the request data object that is passed.

So making a new event chain consists of the following steps:

1. add an entry to *EventType*.
2. add this entry to the *get_compatible_events()* method of the events you want to chain
3. Check that the priorities of the changed events have no ambiguities.
   1. Note that the priority range is filled sparsely. So an increment can solve the ambiguity, as long as it does not break other chains
4. create a concrete class inheriting *AbstractRequest*.
5. Put the entry in *EventType* in this class' *get_event_type()*
6. Put the attributes in the class that the Events expect/modify.