from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

from src.handlers.Dispatcher import Dispatcher
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.request_data.SendPhonemeRequest import SendPhonemeRequest
from src.models.request_data.SendSentenceRequest import SendSentenceRequest
from src.models.CMUPhonemes import CMUPhonemes
from src.helpers.Logger import Logger
from src.modules.ArduinoConnection import ArduinoConnection


import os
import json
from functools import wraps

app = Flask(__name__)
CORS(app)
BASE_URL = '/api/v1'
RESOURCES = os.getcwd() + '\\resources\\'
production = False

# =============================================================================
#  Runtime configuration

# init event dispatcher
dispatcher = Dispatcher()

# config singleton ArduinoConnection
ArduinoConnection().connect_with_config(RESOURCES + 'arduino_config.json')

# load the phoneme patterns 
phoneme_patterns = {}

# loop through available phoneme patterns
for pattern_file in os.listdir(RESOURCES + '\\phoneme_patterns\\'):
    #get phoneme name
    phoneme = pattern_file.replace('.json', '')

    # CMUPhonemes are the phonemes supported in nltk.cmudict()
    if not (phoneme in CMUPhonemes): 
        raise NameError('The resource ' + phoneme + '.json is not a valid phoneme name')

    # load all patterns. This means if change of patterns, restart
    with open(RESOURCES + '\\phoneme_patterns\\' + pattern_file, 'r') as f:
        json_pattern = json.load(f)
    phoneme_patterns[phoneme] = json_pattern

# =============================================================================
#  API ENDPOINT       

# wrapper for json posts
def validate_json(f):
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


if production:
    @app.route('/')
    def standard_route():
        return render_template("index.html")

    @app.errorhandler(404)
    @app.errorhandler(500)
    def error_route(e):
        return render_template("index.html")

"""
GET list of available phonemes
"""
@app.route(BASE_URL + '/phonemes')
def phonemes():
    # all keys are available phonemes
    available = list(phoneme_patterns.keys())

    # return json data and succes code
    return jsonify({'phonemes' : available}), 200


"""
POST sending phoneme(s) to the microcontroller
"""
@app.route(BASE_URL + '/microcontroller/phonemes', methods=['POST'])
@validate_json
def send_phonemes():
    # get body from api
    data = request.json

    # issue events to micrcontroller
    for phoneme in data['phonemes']: 
        # get the json pattern for the phoneme
        json_pattern = phoneme_patterns[phoneme]

        # make the event request data
        send_phoneme_request = SendPhonemeRequest(phoneme, json_pattern)
        # send to dispatcher
        dispatcher.handle(send_phoneme_request)

    # empty body return, succes code
    return "", 200

"""
POST send word(s) to the microcontroller
"""
@app.route(BASE_URL + '/microcontroller/words', methods=['POST'])
@validate_json
def send_words():
    # get body from api
    data = request.json

    # issue events to micrcontroller
    sentence_request = SendSentenceRequest(data['words'], phoneme_patterns)
    dispatcher.handle(sentence_request)

    # create result json with alle sent phonemes
    result = {}
    result["words"] = []
    for decomposition in sentence_request.result:
        result["words"].append({ "phonemes" : decomposition})

    # send return, succes code
    return jsonify(result), 200

##For testing
@app.route(BASE_URL + '/print/', methods=['POST'])
def test():
    if request.method == 'POST':

        phoneme_request = PhonemeTransformRequest()
        phoneme_request.sentences = [request.form['text']]
        dispatcher.handle(phoneme_request)

        return '200'

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
