import io

from events.AbstractEvent import AbstractEvent
from models.EventTypeEnum import EventType
from models.request_data.AbstractRequest import AbstractRequest
from models.request_data.TranscribeRequest import TranscribeRequest
from modules.google_api.GoogleApiWrapper import GoogleApiWrapper

from google.cloud import speech


class GoogleTranscribeEvent(AbstractEvent):
    """
    Transforms a local audio file into text written in given source language.
    """

    PRIORITY: int = 200

    def __init__(self):
        self.client = speech.SpeechClient()

    def handle(self, request_data: AbstractRequest):
        if not GoogleApiWrapper().authenticated:
            raise AssertionError("GoogleTranscribeEvent.handle: make sure to authenticate with the Google API by "
                                 "setting your credentials correctly.")

        if not isinstance(request_data, TranscribeRequest):
            raise ValueError("GoogleTranscribeEvent.handle: request_data is of type " + str(type(request_data)) + ".")

        with io.open(request_data.path, "rb") as audio_file:
            content = audio_file.read()

        audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            request_data.audio_type,
            language_code=request_data.spoken_language
        )

        response = self.client.recognize(config=config, audio=audio)

        # Each result is for a consecutive portion of the audio. Iterate through
        # them to get the transcripts for the entire audio file.
        request_data.sentences = response.results

    @staticmethod
    def get_priority() -> int:
        return GoogleTranscribeEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> [EventType]:
        return [
            EventType.TRANSCRIBE_USING_GOOGLE_API
        ]