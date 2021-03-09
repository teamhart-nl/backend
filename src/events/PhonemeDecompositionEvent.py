from src.models.EventTypeEnum import EventType
from src.events.AbstractEvent import AbstractEvent
from src.helpers.Logger import Logger
from src.models.CMUPhonemes import MappingCMUtoReed
from src.models.request_data.AbstractRequest import AbstractRequest

import nltk

from typing import List


# Initialize arpabet dictionary
try:
    arpabet = nltk.corpus.cmudict.dict()
except LookupError:
    nltk.download('cmudict')
    arpabet = nltk.corpus.cmudict.dict()
    Logger.log_info("ARPABET downloaded!")


class PhonemeDecompositionEvent(AbstractEvent):
    """
    Transforms English sentences into phonemes

    @expects data to have a attribute sentences, which is a list of strings, each string being a word.
    @creates phonemes on the data.
    """

    PRIORITY: int = 100

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
                    arpabet_return = arpabet[str(word).lower()]
                    Logger.log_info("Sentence was decomposed to following (CMU) phonemes")
                    Logger.log_info(arpabet_return)

                    # all the valid decompositions (consisting of CMU phonemes coupled to Reeds)
                    valid_decompositions = []
                    
                    # process each possible decompositions
                    for cmu_decomposition in arpabet_return:
                        # wether the decomposition is valid
                        decomposition_valid = True

                        # decomposition translated to Reed's phonemes
                        reed_decomposition = []

                        for i in range(len(cmu_decomposition)):
                            # remove intonation digits
                            cmu_decomposition[i] = ''.join([i for i in cmu_decomposition[i] if not i.isdigit()])
                            try:
                                reed_decomposition.append(MappingCMUtoReed[cmu_decomposition[i]])
                            except KeyError:
                                # If the phoneme is not known, the decomposition is not valid
                                decomposition_valid = False
                                break

                        if decomposition_valid:
                            valid_decompositions.append(reed_decomposition)

                    # check if there are valid decompositions
                    if len(valid_decompositions) == 0:
                        raise KeyError("No decompositions in CMU Phonemes with Reed equivalent")

                    # set phoneme translation to request data
                    sentence_decomposition.append(valid_decompositions)
                except KeyError:
                    # If the word is not in the Arpabet/ no valid decompositions, continue processing, but log warning
                    Logger.log_warning("PhonemeDecompositionEvent.handle: Word '" + str(word).lower()
                                       + "' was not found in Arpabet dictionary.")

            # add this sentence decomposition to request_data
            request_data.phonemes.append(sentence_decomposition)

        # Log completion information
        Logger.log_info("PhonemeDecompositionEvent.handle: Completed PhonemeDecompositionEvent with (REED) phonemes:")
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
