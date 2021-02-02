from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest

from typing import Dict, Any

class SendPhonemeRequest(AbstractRequest):
    """
    Request type for sending a phoneme to the microcontroller
    """

    # which phoneme
    phoneme : str

    # json representation of phoneme pattern
    phoneme_pattern: Dict[str, Any]

    def __init__(self, phoneme : str, phoneme_pattern : Dict[str, Any]):
        self.phoneme = phoneme
        self.phoneme_pattern = phoneme_pattern

    def get_event_type(self) -> EventType:
        return EventType.SEND_PHONEME_TO_MICROCONTROLLER