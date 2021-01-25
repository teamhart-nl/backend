from models.EventTypeEnum import EventType
from models.request_data.AbstractRequest import AbstractRequest

from google.cloud import speech

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
    sentences: [str]

    def __init__(self, path: str, spoken_language: str):
        if not path or path == "":
            raise ValueError("TranscribeRequest.__init__: path variable is " + path)

        self.path = path
        self.sentences = []

        self.audio_type = speech.RecognitionConfig.AudioEncoding.FLAC
        self.spoken_language = spoken_language

    def get_event_type(self) -> EventType:
        return EventType.TRANSCRIBE_USING_GOOGLE_API
