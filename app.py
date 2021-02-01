from flask import Flask, request, jsonify
from flask_cors import CORS

from src.handlers.Dispatcher import Dispatcher
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.CMUPhonemes import CMUPhonemes

import os

app = Flask(__name__)
CORS(app)

dispatcher = Dispatcher()

BASE_URL = '/api/v1'

## API routes
@app.route(BASE_URL + '/phonemes')
def phonemes():
    available = []
    for file in os.listdir(os.getcwd() + '\\resources\\phoneme_patterns'):
        phoneme = file.replace(".json", "")
        if phoneme in CMUPhonemes:
            available.append(phoneme)

    return jsonify({'phonemes' : available}), 200

@app.route(BASE_URL + '/microcontroller/phonemes', methods=['POST'])
def send_phonemes():
    if request.method == 'POST':

        for phoneme in list(request.form['phonemes']):
            print("TODO: add SendPhonemeEvent {} to the Dispatcher".format(phoneme))

        return '200'

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
