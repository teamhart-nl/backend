from src.events.AbstractEvent import AbstractEvent

from google.cloud import translate_v2 as translate
import six

from typing import List

from src.helpers.Logger import Logger
from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest
from src.models.request_data.TranslateRequest import TranslateRequest
from src.modules.google_api.GoogleApiWrapper import GoogleApiWrapper


class GoogleTranslateEvent(AbstractEvent):
    """
    Translates an array of sentences to another language
    """

    PRIORITY: int = 190

    def __init__(self):
        self.translate_client = translate.Client()

    def handle(self, request_data: AbstractRequest):
        # Check if the Google API wrapper is authenticated
        if not GoogleApiWrapper().authenticated:
            raise AssertionError("GoogleTranslateEvent.handle: make sure to authenticate with the Google API by "
                                 "setting your credentials correctly.")

        # Check if the request_data is of type TranslateRequest
        if not isinstance(request_data, TranslateRequest):
            raise ValueError("GoogleTranslateEvent.handle: request_data is of type " + str(type(request_data)) + ".")

        # Define local string decode function
        def decode(sen: str) -> str:
            if isinstance(sen, six.binary_type):
                return sen.decode("utf-8")

        # Decode sentences using map
        decoded_sentences = map(decode, request_data.original_sentences)

        # Define local translation decode function
        def translate_sentence(sen: str) -> str:
            return self.translate_client.translate(sen, request_data.source_language, request_data.target_language)

        # Translate each of the sentences in the request data
        request_data.translated_sentences = map(translate_sentence, decoded_sentences)

        # Log information
        Logger.log_info("GoogleTranslateEvent.handle: Completed GoogleTranslateEvent with translated sentences:")
        Logger.log_info(request_data.translated_sentences)

        # Return request_data
        return request_data

    @staticmethod
    def get_priority() -> int:
        return GoogleTranslateEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> List[EventType]:
        return [
            EventType.TRANSLATE_USING_GOOGLE_API,
            EventType.COMPLETE_GOOGLE_API_PHONEME_TRANSFORMATION
        ]
