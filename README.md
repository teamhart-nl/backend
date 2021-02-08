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
<summary>/microcontroller/phoneme</summary>

//NOT IMPLEMENTED
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