from flask import request, jsonify

from definitions import API_BASE_URL, RESOURCES
from src.helpers.LoadPhonemeJsonHelper import get_phoneme_patterns
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.request_data.TranslateRequest import TranslateRequest
from src.models.request_data.TranscribeAndTranslateRequest import TranscribeAndTranslateRequest
from src.routes.RouteValidation import validate_json

from werkzeug.utils import secure_filename
import os
import io

from app import app, dispatcher


# =============================================================================
#  Phonemes
# =============================================================================


@app.route(API_BASE_URL + '/phonemes')
def phonemes():
    """
    GET list of available phonemes
    """

    # all keys are available phonemes
    available = list(get_phoneme_patterns(RESOURCES).keys())

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
    request_data = PhonemeTransformRequest(phonemes=data['phonemes'])

    # send to dispatcher
    try:
        dispatcher.handle(request_data)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/phonemes: Could not handle PhonemeTransformRequest successfully", 500

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
    sentence_request = PhonemeTransformRequest(sentences=[data['words']])
    try:
        dispatcher.handle(sentence_request)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/words: Could not handle PhonemeTransformRequest successfully", 500

    # create result json with all sent phonemes
    result = {"words": data['words'], "decomposition": []}
    for decomposition in sentence_request.sent_phonemes:
        result["decomposition"].append({"phonemes": decomposition})

    # send return, success code
    return jsonify(result), 200


@app.route(API_BASE_URL + "/microcontroller/sentences", methods=['POST'])
@validate_json
def send_sentences():
    """
    POST send sentence(s) to the microcontroller
    """

    # get body from api
    data = request.json

    # issue translate event
    translate_request = TranslateRequest(original_sentences=data['sentences'], source_language=data['language'])
    try:
        translate_request = dispatcher.handle(translate_request)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/sentences: Could not handle TranslateRequest successfully", 500

    # Issue decomposition into phonemes and sending to microcontroller
    decomposition_request = PhonemeTransformRequest(sentences=translate_request.translated_sentences)
    try:
        dispatcher.handle(decomposition_request)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/sentences: Could not handle PhonemeTransformRequest successfully", 500

    result = {
        "sentences": translate_request.original_sentences,
        "translation": translate_request.translated_sentences,
    }

    # send return, success code
    return jsonify(result), 200

@app.route(API_BASE_URL + "/microcontroller/audiopath", methods=['POST'])
@validate_json
def send_audiopath():
    """
    POST send sentence(s) to the microcontroller
    """

    # get body from api
    data = request.json

    audio_file = io.open(data['path'], "rb")

    # issue translate event
    transcribe_translate_request = TranscribeAndTranslateRequest(
        audio_file,
        source_language=data['source_language'],
        target_language=data['target_language'])
    try:
        dispatcher.handle(transcribe_translate_request)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/audiopath: Could not handle TranslateRequest successfully", 500

    audio_file.close()

    # Issue decomposition into phonemes and sending to microcontroller
    decomposition_request = PhonemeTransformRequest(sentences=transcribe_translate_request.translated_sentences)
    try:
        dispatcher.handle(decomposition_request)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/audiopath: Could not handle PhonemeTransformRequest successfully", 500

    result = {
        "transcription": transcribe_translate_request.original_sentences,
        "translation": transcribe_translate_request.translated_sentences,
    }

    # send return, success code
    return jsonify(result), 200


@app.route("/microcontroller/audiofile", methods=["POST"])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        return "", 400

    file = request.files['file']
    # if user does not select file, browser also
    # submit an empty part without filename
    # if file:
    #     filename = os.path.join(RESOURCES, secure_filename(file.filename))
    #     file.save(filename)

    # issue translate event
    transcribe_translate_request = TranscribeAndTranslateRequest(
        file,
        source_language='nl',
        target_language='en')
    try:
        dispatcher.handle(transcribe_translate_request)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/audiofile: Could not handle TranslateRequest successfully", 500

    # Issue decomposition into phonemes and sending to microcontroller
    decomposition_request = PhonemeTransformRequest(sentences=transcribe_translate_request.translated_sentences)
    try:
        dispatcher.handle(decomposition_request)
    except RuntimeError:
        return API_BASE_URL + "/microcontroller/audiofile: Could not handle PhonemeTransformRequest successfully", 500

    result = {
        "transcription": transcribe_translate_request.original_sentences,
        "translation": transcribe_translate_request.translated_sentences,
    }

    # send return, success code
    return jsonify(result), 200
