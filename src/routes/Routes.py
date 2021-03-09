from flask import request, jsonify

from definitions import API_BASE_URL
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.routes.RouteValidation import validate_json

from app import app, dispatcher, phoneme_patterns


# =============================================================================
#  Phonemes
# =============================================================================


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
    print("hey")

    # get body from api
    data = request.json

    # make the event request data
    request_data = PhonemeTransformRequest(phoneme_patterns, phonemes=data['phonemes'])

    # send to dispatcher
    dispatcher.handle(request_data)

    # empty body return, success code
    return "", 200


# =============================================================================
#  Words
# =============================================================================


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

