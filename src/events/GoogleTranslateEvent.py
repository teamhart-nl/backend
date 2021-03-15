from src.events.AbstractEvent import AbstractEvent

from google.cloud import translate
import html

from typing import List

from src.helpers.Logger import Logger
from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest
from src.modules.google_api.GoogleApiWrapper import GoogleApiWrapper


class GoogleTranslateEvent(AbstractEvent):
    """
    Translates an array of sentences to another language
    """

    PRIORITY: int = 190

    def __init__(self):
        self.translate_client = translate.TranslationServiceClient()

    def handle(self, request_data: AbstractRequest):
        # Check if the Google API wrapper is authenticated
        if not GoogleApiWrapper().authenticated:
            raise AssertionError("GoogleTranslateEvent.handle: make sure to authenticate with the Google API by "
                                 "setting your credentials correctly.")

        # Define local translation decode function
        def translate_sentence(sen: str) -> str:
            return html.unescape(
                self.translate_client.translate_text(
                    contents=[sen],  # sentence(s) to be translated
                    parent="projects/solid-century-301518/locations/global",  # Name of project in google cloud
                    source_language_code=request_data.source_language,  # Source language
                    target_language_code=request_data.target_language  # Target language
                ).translations[0].translated_text
            )

        if request_data.source_language == request_data.target_language:
            # If source language is equal to target language, then no translation needs to happen.
            request_data.translated_sentences = request_data.original_sentences
            Logger.log_info("Sentences were not translated as source and target language were equal.")
        else:
            # Translate each of the sentences in the request data
            Logger.log_info(
                "Translating '" + str(request_data.original_sentences) + "' to " + request_data.target_language)
            request_data.translated_sentences = list(map(translate_sentence, request_data.original_sentences))

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
            EventType.TRANSCRIBE_AND_TRANSLATE_USING_GOOGLE_API,
            EventType.COMPLETE_GOOGLE_API_PHONEME_TRANSFORMATION
        ]
