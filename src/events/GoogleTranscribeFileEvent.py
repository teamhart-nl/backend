from events.AbstractEvent import AbstractEvent
from models.EventTypeEnum import EventType
from models.request_data.AbstractRequest import AbstractRequest
from models.request_data.TranscribeRequest import TranscribeRequest


class GoogleTranscribeEvent(AbstractEvent):
    """
    Transforms a local audio file into text written in given source language.
    """

    PRIORITY: int = 200

    def __init__(self):
        pass

    def handle(self, request_data: AbstractRequest):
        if not isinstance(request_data, TranscribeRequest):
            raise ValueError("GoogleTranscribeEvent.handle: request_data is of type " + str(type(request_data)) + ".")

    @staticmethod
    def get_priority() -> int:
        return GoogleTranscribeEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> [EventType]:
        return [
            EventType.TRANSCRIBE_USING_GOOGLE_API
        ]