from flask import Flask, render_template, request
from flask_cors import CORS

from src.handlers.Dispatcher import Dispatcher
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest

app = Flask(__name__)
CORS(app)

dispatcher = Dispatcher()

BASE_URL = "/api/v1/"

@app.route('/vue-test')
def vue_test():
    return {"greeting": "Hello from Flask!"}


@app.route('/print/', methods=['POST'])
def test():
    if request.method == 'POST':

        phoneme_request = PhonemeTransformRequest()
        phoneme_request.sentences = [request.form['text']]
        dispatcher.handle(phoneme_request)

        return '200'


#routes
#GET pattern for a phoneme
#param 

#GET phonemes for sentence
#described above

#GET status of arduino
#result: arduino status, motor status? idk if that accessible

#POST phonemes for a given sentence
#param: sl
#param: tl
#body: sentence
#returns: phonemes (or patterns?)
#effects: arduino fires full sentence

#GET list of phonemes
#phonemes with identifiable ID's 

#GET stop arduino
#effects: stops all motors from firing

#GEt test arduino
#effects: buzzes all motors

#POST send single phoneme 
#param: uniquely identifiable phoneme
#returns: success or notFound
#effects: arduino


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
