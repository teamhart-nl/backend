from src.events.AbstractEvent import AbstractEvent
from src.models.request_data import AbstractRequestData
from src.models.EventTypeEnum import EventType

import nltk


class ArpabetPhonemeEvent(AbstractEvent):
    """
    Transforms an English sentence into phonemes
    """

    def __init__(self):
        try:
            self.arpabet = nltk.corpus.cmudict.dict()
        except LookupError:
            nltk.download('cmudict')
            self.arpabet = nltk.corpus.cmudict.dict()

    def handle(self, event_type: EventType, request_data: AbstractRequestData):
        # TODO check if request is from correct concrete class
        print()
