from flask import Flask, request, jsonify
from flask_cors import CORS

from src.handlers.Dispatcher import Dispatcher
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.request_data.SendPhonemeRequest import SendPhonemeRequest
from src.models.CMUPhonemes import CMUPhonemes

import os
import json
from functools import wraps

app = Flask(__name__)
CORS(app)

dispatcher = Dispatcher()

BASE_URL = '/api/v1'

#Wrapper for json posts
def validate_json(f):
    @wraps(f)
    def wrapper(*args, **kw):
        try:
            data = request.json
        except Exception: #problem reading in json
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        if data is None:  #empty while json is expected
            msg = "payload must be a valid json"
            return jsonify({"error": msg}), 400
        else:    
            return f(*args, **kw)
    return wrapper

## API routes
@app.route(BASE_URL + '/phonemes')
def phonemes():
    available = [] #list of available phonemes
    fp = os.getcwd() + '\\resources\\phoneme_patterns' #resource folder for patterns of phonemes

    #loop through all 
    for file in os.listdir(fp):
        phoneme = file.replace(".json", "")
        
        if phoneme in CMUPhonemes: #CMUPhonemes are the phonemes supported in nltk.cmudict()
            available.append(phoneme)
        else:
            print(phoneme + ' is not a valid phoneme name')

    return jsonify({'phonemes' : available}), 200

@app.route(BASE_URL + '/microcontroller/phonemes', methods=['POST'])
@validate_json
def send_phonemes():
        #get body from api
        data = request.json

        for phoneme in data['phonemes']: #issue events to micrcontroller
            #load the json of the phoneme
            json_fp = os.getcwd() + '\\resources\\phoneme_patterns\\' + phoneme + ".json"
            with open(json_fp, 'r') as f:
                json_pattern = json.load(f)
            #make the event request data
            phoneme_request = SendPhonemeRequest(phoneme, json_pattern)
            #send to dispatcher
            Dispatcher.handle(phoneme_request)

        return "", 200

##For testing
@app.route('/vue-test')
def vue_test():
    return {"greeting": "From Flask, With Love"}


@app.route(BASE_URL + '/print/', methods=['POST'])
def test():
    if request.method == 'POST':

        phoneme_request = PhonemeTransformRequest()
        phoneme_request.sentences = [request.form['text']]
        dispatcher.handle(phoneme_request)

        return '200'

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
