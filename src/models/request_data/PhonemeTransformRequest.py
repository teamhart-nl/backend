from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest


class PhonemeTransformRequest(AbstractRequest):

    sentences: [str]
    phonemes: [[[[str]]]]

    def __init__(self, sentences=None):
        if sentences is None:
            sentences = []

        self.sentences = sentences

    def get_event_type(self) -> EventType:
        return EventType.TRANSFORM_TEXT_INTO_PHONEMES
