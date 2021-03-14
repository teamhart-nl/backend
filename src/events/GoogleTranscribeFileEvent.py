import io

from src.events.AbstractEvent import AbstractEvent
from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest
from src.modules.google_api.GoogleApiWrapper import GoogleApiWrapper

from google.cloud import speech

from typing import List


class GoogleTranscribeEvent(AbstractEvent):
    """
    Transforms a local audio file into text written in given source language.
    """

    PRIORITY: int = 200

    def __init__(self):
        self.client = speech.SpeechClient()

    def handle(self, request_data: AbstractRequest):

        # Check if the google api wrapper is authenticated
        if not GoogleApiWrapper().authenticated:
            raise AssertionError("GoogleTranscribeEvent.handle: make sure to authenticate with the Google API by "
                                 "setting your credentials correctly.")

        # read the audio file
        content = request_data.audio_file.read()

        # Get audio content
        audio = speech.RecognitionAudio(content=content)

        # Set audio configuration
        config = speech.RecognitionConfig(
            language_code=request_data.source_language
        )

        # Get Google API response
        response = self.client.recognize(config=config, audio=audio)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        request_data.original_sentences = []
        for sentence in response.results:
            request_data.original_sentences.append(sentence.alternatives[0].transcript)

        return request_data

    @staticmethod
    def get_priority() -> int:
        return GoogleTranscribeEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> List[EventType]:
        return [
            EventType.TRANSCRIBE_USING_GOOGLE_API,
            EventType.TRANSCRIBE_AND_TRANSLATE_USING_GOOGLE_API,
            EventType.COMPLETE_GOOGLE_API_PHONEME_TRANSFORMATION]
