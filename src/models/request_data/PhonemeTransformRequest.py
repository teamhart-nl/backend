from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest


class PhonemeTransformRequest(AbstractRequest):
    """
    Request type for a transformation that includes a phonemes transformation.
    """

    # List of sentences
    sentences: [str]

    # List of phonemes for each possibility of a word, for each word in a sentence, for each sentence in the message
    phonemes: [[[[str]]]]

    def __init__(self, sentences=None):
        if sentences is None:
            sentences = []

        self.sentences = sentences

    def get_event_type(self) -> EventType:
        return EventType.TRANSFORM_TEXT_INTO_PHONEMES
