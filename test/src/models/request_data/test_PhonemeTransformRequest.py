from src.models.EventTypeEnum import EventType
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest, split_sentences

import pytest


def test_split_sentences():
    ss = split_sentences(["sentence one", "sentence two"])

    assert ss[0][0] == "sentence"
    assert ss[0][1] == "one"
    assert ss[1][0] == "sentence"
    assert ss[1][1] == "two"


def test_split_sentences_edge():
    ss = split_sentences([])

    assert len(ss) == 0


def test_constructor_error_1():
    with pytest.raises(ValueError,
                       match="PhonemeTransformRequest.__init__: phoneme_patterns cannot be None"):
        PhonemeTransformRequest(None)


def test_constructor_error_2():
    with pytest.raises(ValueError,
                       match="PhonemeTransformRequest.__init__: both sentences and phonemes parameter was passed"):
        PhonemeTransformRequest({}, ["sentence"], ["Pho"])


def test_constructor_standard_case_1_1():
    ptr = PhonemeTransformRequest({}, ["first sentence", "second sentence"])

    assert ptr.sentences[0][0] == "first"
    assert ptr.sentences[0][1] == "sentence"
    assert ptr.sentences[1][0] == "second"
    assert ptr.sentences[1][1] == "sentence"


def test_constructor_standard_case_1_2():
    ptr = PhonemeTransformRequest({}, [["first", "sentence"], ["second", "sentence"]])

    assert ptr.sentences[0][0] == "first"
    assert ptr.sentences[0][1] == "sentence"
    assert ptr.sentences[1][0] == "second"
    assert ptr.sentences[1][1] == "sentence"


def test_constructor_standard_case_1_edge():
    ptr = PhonemeTransformRequest({}, sentences=[])

    # ptr.sentences == []
    assert len(ptr.sentences) == 0


def test_constructor_standard_case_2():
    ptr = PhonemeTransformRequest({}, phonemes=["PHO1", "PHO2"])

    assert ptr.phonemes[0][0][0][0] == "PHO1"
    assert ptr.phonemes[0][0][0][1] == "PHO2"


def test_get_event_type_case_1_constructor():
    ptr = PhonemeTransformRequest({}, sentences=["some sentence"])

    assert ptr.get_event_type() == EventType.SEND_SENTENCES_TO_MICROCONTROLLER


def test_get_event_type_case_2_constructor():
    ptr = PhonemeTransformRequest({}, phonemes=["PHO1"])

    assert ptr.get_event_type() == EventType.SEND_PHONEMES_TO_MICROCONTROLLER
