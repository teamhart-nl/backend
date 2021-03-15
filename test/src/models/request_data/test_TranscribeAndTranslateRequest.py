from src.models.EventTypeEnum import EventType
from src.models.request_data.TranscribeAndTranslateRequest import TranscribeAndTranslateRequest

import pytest

def test_constructor_error_1():
    with pytest.raises(ValueError,
                       match="TranscribAndTranslateRequest.__init__: no source language passed"):
        TranscribeAndTranslateRequest(audio_file=object, original_sentences=object)

def test_constructor_error_2():
    with pytest.raises(ValueError,
                       match="TranscribAndTranslateRequest.__init__: no audio file or sentences passed"):
        TranscribeAndTranslateRequest(source_language='en')

def test_constructor_standard_case_1():
    ptr = TranscribeAndTranslateRequest(original_sentences=["first sentence", "second sentence"], source_language='en')

    assert ptr.original_sentences[0] == "first sentence"
    assert ptr.original_sentences[1] == "second sentence"

def test_get_event_type_case_1_constructor():
    ptr = TranscribeAndTranslateRequest(original_sentences=["some sentence"], source_language='en')

    assert ptr.get_event_type() == EventType.TRANSLATE_USING_GOOGLE_API


def test_get_event_type_case_2_constructor():
    ptr = TranscribeAndTranslateRequest(audio_file=object, source_language='en')

    assert ptr.get_event_type() == EventType.TRANSCRIBE_AND_TRANSLATE_USING_GOOGLE_API
