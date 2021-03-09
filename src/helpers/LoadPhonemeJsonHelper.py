import json
import os

from src.models.CMUPhonemes import REEDPhonemes


def get_phoneme_patterns(resources: str):
    """
    load the phoneme patterns
    """

    patterns = {}

    # loop through available phoneme patterns
    for pattern_file in os.listdir(os.path.join(resources, 'phoneme_patterns')):
        # pattern file should be json
        if pattern_file[-5::] != '.json':
            raise OSError('The resource ' + pattern_file + ' is not a json file')

        # get phoneme name
        phoneme = pattern_file.replace('.json', '')

        # CMUPhonemes are the phonemes supported in nltk.cmudict()
        if not (phoneme in REEDPhonemes):
            raise NameError('The resource ' + phoneme + '.json is not a valid phoneme name')

        # load all patterns. This means if change of patterns, restart
        with open(os.path.join(resources, 'phoneme_patterns', pattern_file), 'r') as f:
            json_pattern = json.load(f)
        patterns[phoneme] = json_pattern

    return patterns