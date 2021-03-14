from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest

from google.cloud import speech

from typing import List


class TranscribeRequest(AbstractRequest):
    """
    Request type for a transformation that includes a transcription from an Audio file to sentences
    """

    # Path to audio file
    path: str

    # Type of audio file
    audio_type: any

    # Spoken language
    spoken_language: str

    # Transcription
    sentences: List[str]

    def __init__(self, path_to_local_audio_file: str, spoken_language: str):
        if not path_to_local_audio_file or path_to_local_audio_file == "":
            raise ValueError("TranscribeRequest.__init__: path variable is " + path_to_local_audio_file)

        self.path = path_to_local_audio_file
        self.sentences = []

        self.audio_type = speech.RecognitionConfig.AudioEncoding.FLAC
        self.spoken_language = spoken_language

    def get_event_type(self) -> EventType:
        return EventType.TRANSCRIBE_USING_GOOGLE_API
