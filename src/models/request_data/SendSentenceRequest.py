from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest

from typing import Dict, Any, List


class SendSentenceRequest(AbstractRequest):
    """
    Request type for sending words (broken down into phonemes) to the microcontroller
    """

    # Sentence as list of words
    words: [str]

    # List of phonemes for each possibility of a word, for each word in a sentence,
    phonemes: [[[str]]]

    # Mapping of phoneme to the JSON pattern
    phoneme_patterns: Dict[str, Dict[str, Any]]

    # the pattern combinations that were sent to the arduino
    result: List[List[str]]

    def __init__(self, sentence: List[str], patterns : Dict[str, Dict[str, Any]]):
        self.words = sentence
        self.phoneme_patterns = patterns
        self.result = []

    def get_event_type(self) -> EventType:
        return EventType.SEND_SENTENCE_TO_MICROCONTROLLER
