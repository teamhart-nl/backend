from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest

from typing import List

class TranslateRequest(AbstractRequest):
    """
    Request type for a transformation that includes a translation of sentences.
    """

    # Sentences to be translated
    original_sentences: List[str]

    # Stores the translated sentences after translation
    translated_sentences: List[str]

    # The original language code of the sentences
    source_language: str

    # The target language code
    target_language: str

    def __init__(self, original_sentences, source_language, target_language="en"):
        # Initialize all the variables
        self.original_sentences = original_sentences
        self.source_language = source_language
        self.target_language = target_language
        self.translated_sentences = []

    def get_event_type(self) -> EventType:
        return EventType.TRANSLATE_USING_GOOGLE_API
