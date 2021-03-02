from src.events.PhonemeDecompositionEvent import PhonemeDecompositionEvent
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest


def test_handle_basic_case_1():
    ptr = PhonemeTransformRequest({}, sentences=[["heat"]])

    ev = PhonemeDecompositionEvent()

    request_data = ev.handle(ptr)

    assert request_data.phonemes[0][0][0][0] == "H"
    assert request_data.phonemes[0][0][0][1] == "EE"
    assert request_data.phonemes[0][0][0][2] == "T"


def test_handle_basic_case_2():
    ptr = PhonemeTransformRequest({}, sentences=[["big", "heat"]])

    ev = PhonemeDecompositionEvent()

    request_data = ev.handle(ptr)

    assert request_data.phonemes[0][0][0][0] == "B"
    assert request_data.phonemes[0][1][0][0] == "H"


def test_handle_basic_case_3():
    ptr = PhonemeTransformRequest({}, sentences=["sentence one"])

    ev = PhonemeDecompositionEvent()

    request_data = ev.handle(ptr)

    assert request_data.phonemes[0][0][0][0] == "S"
    assert request_data.phonemes[0][1][0][0] == "W"
    assert request_data.phonemes[0][1][1][0] == "H"


def test_handle_basic_case_4():
    ptr = PhonemeTransformRequest({}, sentences=["sent", "again"])

    ev = PhonemeDecompositionEvent()

    request_data = ev.handle(ptr)

    assert request_data.phonemes[0][0][0][0] == "S"
    assert request_data.phonemes[1][0][0][0] == "UH"


def test_handle_edge_case_1():
    ptr = PhonemeTransformRequest({}, sentences=[])

    ev = PhonemeDecompositionEvent()

    request_data = ev.handle(ptr)

    assert len(request_data.phonemes) == 0


def test_handle_edge_case_2():
    ptr = PhonemeTransformRequest({}, sentences=["as;liked"])

    ev = PhonemeDecompositionEvent()

    request_data = ev.handle(ptr)

    assert len(request_data.phonemes[0]) == 0
