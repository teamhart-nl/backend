from src.models.EventTypeEnum import EventType
from src.models.request_data.AbstractRequest import AbstractRequest

from google.cloud import speech

from typing import List, BinaryIO


class TranscribeAndTranslateRequest(AbstractRequest):
    """
    Request type for a transformation that includes a transcription from an Audio file to sentences
    """

    # Path to audio file
    path: str

    # audio file
    audio_file: BinaryIO

    # Type of audio file
    audio_type: any

    # Spoken language
    source_language: str

    # The target language code
    target_language: str

    # Transcription
    original_sentences: List[str]

    # Stores the translated sentences after translation
    translated_sentences: List[str]

    # The original language code of the sentences
    source_language: str

    def __init__(self, audio_file: BinaryIO, source_language: str, target_language: str = 'en'):
        if not audio_file:
            raise ValueError("TranscribeRequest.__init__: no audio file is passed")

        self.audio_file = audio_file

        self.source_language = source_language
        self.target_language = target_language

        self.original_sentences = []
        self.translated_sentences = []

        self.audio_type = speech.RecognitionConfig.AudioEncoding.FLAC

    def get_event_type(self) -> EventType:
        return EventType.TRANSCRIBE_AND_TRANSLATE_USING_GOOGLE_API
