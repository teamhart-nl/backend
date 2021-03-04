from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from src.handlers.Dispatcher import Dispatcher
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.CMUPhonemes import REEDPhonemes
from src.modules.ArduinoConnection import ArduinoConnection

from definitions import PRODUCTION, RESOURCES, API_BASE_URL

import os
import json
from functools import wraps

app = Flask(__name__)
CORS(app)

# =============================================================================
#  Runtime configuration

# init event dispatcher
dispatcher = Dispatcher()

# config singleton ArduinoConnection
ArduinoConnection().connect_with_config(os.path.join(RESOURCES, 'arduino_config.json'))

# load the phoneme patterns

def get_phoneme_patterns(resources: str):
    # load the phoneme patterns
    patterns = {}

    # loop through available phoneme patterns
    for pattern_file in os.listdir(os.path.join(resources, 'phoneme_patterns')):
        # pattern file should be json
        if pattern_file[-5::] != '.json':
            raise OSError('The resource ' + pattern_file + ' is not a json file')

        # get phoneme name
        phoneme = pattern_file.replace('.json', '')

        # CMUPhonemes are the phonemes supported in nltk.cmudict()
        if not (phoneme in REEDPhonemes):
            raise NameError('The resource ' + phoneme + '.json is not a valid phoneme name')

        # load all patterns. This means if change of patterns, restart
        with open(os.path.join(resources, 'phoneme_patterns', pattern_file), 'r') as f:
            json_pattern = json.load(f)
        patterns[phoneme] = json_pattern

    return patterns


phoneme_patterns = get_phoneme_patterns(RESOURCES)

# =============================================================================
#  API ENDPOINT

def validate_json(f):
    """
    wrapper for json posts
    """

    @wraps(f)
    def wrapper(*args, **kw):
        try:
            data = request.json
        except Exception:
            # problem reading in json
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        if data is None:
            # empty while json is expected
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        else:
            return f(*args, **kw)

    return wrapper


if PRODUCTION:
    @app.route('/')
    def standard_route():
        return render_template("index.html")

    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_route(e):
        return render_template("index.html")


@app.route(API_BASE_URL + '/phonemes')
def phonemes():
    """
    GET list of available phonemes
    """

    # all keys are available phonemes
    available = list(phoneme_patterns.keys())

    # return json data and success code
    return jsonify({'phonemes': available}), 200


@app.route(API_BASE_URL + '/microcontroller/phonemes', methods=['POST'])
@validate_json
def send_phonemes():
    """
    POST sending phoneme(s) to the microcontroller
    """

    # get body from api
    data = request.json

    # make the event request data
    request_data = PhonemeTransformRequest(phoneme_patterns, phonemes=data['phonemes'])

    # send to dispatcher
    dispatcher.handle(request_data)

    # empty body return, success code
    return "", 200


@app.route(API_BASE_URL + '/microcontroller/words', methods=['POST'])
@validate_json
def send_words():
    """
    POST send word(s) to the microcontroller
    """

    # get body from api
    data = request.json

    # issue event
    sentence_request = PhonemeTransformRequest(phoneme_patterns, sentences=[data['words']])
    dispatcher.handle(sentence_request)

    # create result json with all sent phonemes
    result = {"words": data['words'], "decomposition": []}
    for decomposition in sentence_request.sent_phonemes:
        result["decomposition"].append({"phonemes": decomposition})

    # send return, success code
    return jsonify(result), 200


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
