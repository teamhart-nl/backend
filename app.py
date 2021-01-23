from flask import Flask, render_template, request
from flask_cors import CORS

from src.handlers.Dispatcher import Dispatcher
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest

app = Flask(__name__)
CORS(app)

dispatcher = Dispatcher()


@app.route('/')
def hello_world():
    return render_template('home.html')


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


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
