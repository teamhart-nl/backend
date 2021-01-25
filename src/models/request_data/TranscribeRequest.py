from models.EventTypeEnum import EventType
from models.request_data.AbstractRequest import AbstractRequest


class TranscribeRequest(AbstractRequest):
    """
    Request type for a transformation that includes a transcription from an Audio file to sentences
    """

    # Path to audio file
    path: str

    # Transcription
    sentences: [str]

    def __init__(self, path):
        if not path or path == "":
            raise ValueError("TranscribeRequest.__init__: path variable is " + path)

        self.path = path
        self.sentences = []

    def get_event_type(self) -> EventType:
        return EventType.TRANSCRIBE_USING_GOOGLE_API
