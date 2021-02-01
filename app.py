from flask import Flask, render_template, request
from flask_cors import CORS

from src.handlers.Dispatcher import Dispatcher
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.CMUPhonemes import CMUPhonemes

import os

app = Flask(__name__)
CORS(app)

dispatcher = Dispatcher()

BASE_URL = '/api/v1'

@app.route('/vue-test')
def vue_test():
    return {"greeting": "Hello from Flask!"}


@app.route(BASE_URL + '/print/', methods=['POST'])
def test():
    if request.method == 'POST':

        phoneme_request = PhonemeTransformRequest()
        phoneme_request.sentences = [request.form['text']]
        dispatcher.handle(phoneme_request)

        return '200'

@app.route(BASE_URL + '/phonemes')
def phonemes():
    available = []
    for file in os.listdir(os.getcwd() + '\\resources\\phoneme_patterns'):
        phoneme = file.replace(".json", "")
        if phoneme in CMUPhonemes:
            available.append(phoneme)

    return {'phonemes' : available}, 200

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
