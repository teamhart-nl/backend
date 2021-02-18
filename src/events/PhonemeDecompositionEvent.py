from src.models.EventTypeEnum import EventType
from src.events.AbstractEvent import AbstractEvent
from src.helpers.Logger import Logger
from src.models.request_data.AbstractRequest import AbstractRequest

import nltk

from typing import List


class PhonemeDecompositionEvent(AbstractEvent):
    """
    Transforms English sentences into phonemes

    @expects data to have a attribute sentences, which is a list of strings, each string being a word.
    @creates phonemes on the data.
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

        # Loop over all sentences in the request_data.
        for sentence in request_data.sentences:
            # decomposition for this sentence
            sentence_decomposition = []

            # loop over each word in the sentence
            for word in sentence:
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
                    sentence_decomposition.append(arpabet_return)
                except KeyError:
                    # If the word is not in the Arpabet, continue processing, but log warning
                    Logger.log_warning("PhonemeDecompositionEvent.handle: Word '" + str(word).lower()
                                       + "' was not found in Arpabet dictionary.")

            # add this sentence decomposition to request_data
            request_data.phonemes.append(sentence_decomposition)

        # Log completion information
        Logger.log_info("PhonemeDecompositionEvent.handle: Completed PhonemeDecompositionEvent with phonemes:")
        Logger.log_info(request_data.phonemes)

        # Return request data
        return request_data

    @staticmethod
    def get_priority() -> int:
        return PhonemeDecompositionEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> List[EventType]:
        return [
            EventType.SEND_SENTENCES_TO_MICROCONTROLLER
        ]
