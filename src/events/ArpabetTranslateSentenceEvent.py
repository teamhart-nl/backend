from src.models.request_data.PhonemeTransformRequest import PhonemeTransformRequest
from src.models.EventTypeEnum import EventType
from src.events.AbstractEvent import AbstractEvent
from src.helpers.Logger import Logger
from src.models.request_data.AbstractRequest import AbstractRequest

import nltk


class ArpabetTranslateSentenceEvent(AbstractEvent):
    """
    Transforms an English sentence into phonemes

    expects data to have a attribute words, which is a list of strings, each string being a word.
    creates attribute phonemes on the data.
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
        # Initialize list for phonemes.
        request_data.phonemes = []

        # Loop over all words in the request_data.
        for word in request_data.words:

            try:
                # Try to transform the word into phonemes using the Arpabet and add it to the list
                arpabet_return = self.arpabet[str(word).lower()]

                # remove digits from arpabet return
                # TODO check if this is the way in which we want to handle digits? Wouldn't it be better to write
                #  them out fully?
                for alternative in arpabet_return:
                    for i in range(len(alternative)):
                        alternative[i] = ''.join([i for i in alternative[i] if not i.isdigit()])
                
                # set phoneme translation to request data
                request_data.phonemes.append(arpabet_return)
            except KeyError:
                # If the word is not in the Arpabet, continue processing, but log warning
                Logger.log_warning("ArpabetTranslateSentenceEvent.handle: Word '" + str(word).lower()
                                    + "' was not found in Arpabet dictionary.")

        # Log completion information
        Logger.log_info("ArpabetTranslateSentenceEvent.handle: Completed ArpabetTranslateSentenceEvent with phonemes:")
        Logger.log_info(request_data.phonemes)

        # Return request data
        return request_data

    @staticmethod
    def get_priority() -> int:
        return ArpabetTranslateSentenceEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> [EventType]:
        return [
            EventType.SEND_SENTENCE_TO_MICROCONTROLLER
        ]
