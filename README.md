# backend

Install requirements with `pip install -r /path/to/requirements.txt`

Flask can be run simply with `flask run`

If you want to generate a distribution executable (for perception cluster), this can (after everything is installed) be done with `pyinstaller -F --add-data "templates;templates" --add-data "static;static" app.py` (not elaborately tested yet).

## API Specification

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

    curl -H "Content-Type: application/json" -d "{ \"phonemes\": [\"K\", \"L\"] }" http://localhost:5000/api/v1/microcontroller/phonemes

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

    curl -H "Content-Type: application/json" -d "{ \"words\": [\"Team\", \"HART\"] }" http://localhost:5000/api/v1/microcontroller/words

RESULT:

    {"words" : [
        {
            "phonemes" : ["T", "IY", "M"]
        },

        {
            "phonemes" : ["T", "R", "IY", "T]
        },
    ]}, 
    200 if OK

</details>

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

## Glossary

* phoneme: a string representing a phoneme, full list in models.CMUPhonemes
* phoneme_pattern: Dict/JSON format of the vibrational pattern for a certain phoneme
* decomposition: a word split up in its phonemes
* Word: depending on context either: a string, a list of alternative decompositions, or a list of phonemes
* Sentence: list of words
