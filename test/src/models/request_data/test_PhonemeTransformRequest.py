from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest

import pytest


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


def test_constructor_standard_case_2():
    ptr = PhonemeTransformRequest({}, phonemes=["PHO1", "PHO2"])

    assert ptr.phonemes[0][0][0][0] == "PHO1"
    assert ptr.phonemes[0][0][0][1] == "PHO2"
