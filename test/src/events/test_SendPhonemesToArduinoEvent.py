from src.events.SendPhonemesToArduinoEvent import SendPhonemesToArduinoEvent
from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.modules.ArduinoConnection import ArduinoConnection
from app import get_phoneme_patterns

from definitions import ROOT_DIR, RESOURCES

import os

connection = ArduinoConnection()\
                .connect_with_config(os.path.join(ROOT_DIR, "test\\resources\\arduino_config_test.json"))

phoneme_patters = get_phoneme_patterns(RESOURCES)


def test_handle_basic_case_1():
    ptr = PhonemeTransformRequest(phoneme_patters, phonemes=["HH"])

    request_data = SendPhonemesToArduinoEvent().handle(ptr)

    assert request_data.sent_phonemes[0][0] == "HH"
