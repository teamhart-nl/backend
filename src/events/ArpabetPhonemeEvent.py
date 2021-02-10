from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.EventTypeEnum import EventType
from src.events.AbstractEvent import AbstractEvent
from src.helpers.Logger import Logger
from src.models.request_data.AbstractRequest import AbstractRequest

import nltk


class ArpabetPhonemeEvent(AbstractEvent):
    """
    Transforms an English sentence into phonemes
    """

    PRIORITY: int = 100

    def __init__(self):
        # Initialize arpabet dictionary
        try:
            self.arpabet = nltk.corpus.cmudict.dict()
        except LookupError:
            nltk.download('cmudict')
            self.arpabet = nltk.corpus.cmudict.dict()

    def handle(self, request_data: AbstractRequest):
        # Check if the request)data is of type PhonemeTransformRequest
        if not isinstance(request_data, PhonemeTransformRequest):
            raise ValueError("ArpabetPhonemeEvent.handle: request_data is of type " + str(type(request_data)) + ".")

        # Initialize list for phonemes.
        request_data.phonemes = []

        # Loop over all sentences in the request_data.
        for sentence in request_data.sentences:
            sentence_in_phonemes = []

            # Loop over every word in the sentence.
            for word in sentence.split():
                try:
                    # Try to transform the word into phonemes using the Arpabet and add it to the list
                    sentence_in_phonemes.append(self.arpabet[str(word).lower()])
                except KeyError:
                    # If the word is not in the Arpabet, continue processing, but log warning
                    Logger.log_warning("ArpabetPhonemeEvent.handle: Word '" + str(word).lower()
                                       + "' was not found in Arpabet dictionary.")

            # Add transformation of sentence to list of sentences
            request_data.phonemes.append(sentence_in_phonemes)

        # Log completion information
        Logger.log_info("ArpabetPhonemeEvent.handle: Completed ArpabetPhonemeEvent with phonemes:")
        Logger.log_info(request_data.phonemes)

        # Return request data
        return request_data

    @staticmethod
    def get_priority() -> int:
        return ArpabetPhonemeEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> [EventType]:
        return [
            EventType.TRANSFORM_TEXT_INTO_PHONEMES,
            EventType.COMPLETE_GOOGLE_API_PHONEME_TRANSFORMATION
        ]
