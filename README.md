# backend

Install requirements with `pip install -r /path/to/requirements.txt`

Flask can be run simply with `flask run`

If you want to generate a distribution executable (for perception cluster), this can (after everything is installed) be done with `pyinstaller -F --add-data "templates;templates" --add-data "static;static" app.py` (not elaborately tested yet).

## API Specification

### Phonemes
<details>
<summary>/phonemes</summary>


REQUEST:

    GET /api/v1/phonemes

RESULT:

    {a collection of uniquely identifiable ids}

</details>

### Patterns
<details>
<summary>/patterns/</summary>


REQUEST:

    GET /api/v1/phonemes/

RESULT:

    {the vibrational patterns of each phoneme}

</details>


<details>
<summary>/patterns/phoneme</summary>


REQUEST:

    GET /api/v1/patterns/phoneme

RESULT:

    {get the w}

</details>


### Microcontroller
<details>
<summary>/microcontroller/status</summary>


REQUEST:

    GET /api/v1/microcontroller/status

RESULT:

    {metrics for status}

</details>

<details>
<summary>/microcontroller/stop</summary>

Stop all haptic activity on the microcontroller.

REQUEST:

    GET /api/v1/microcontroller/stop

RESULT:

    {succes or nah}

</details>

<details>
<summary>/microcontroller/phoneme</summary>

Send a phoneme to the microcontroller directly

REQUEST:

    POST /api/v1/microcontroller/stop

BODY:

    {collection of at least one phoneme}

RESULT:

    {succes or nah}

</details>