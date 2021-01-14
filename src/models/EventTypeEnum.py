from enum import Enum

from src.events.ArpabetPhonemeEvent import ArpabetPhonemeEvent


class EventType(Enum):
    """
    Enum for all event types, and their associations to an ordered list of concrete events.
    """

    # TODO list should be filled with events
    COMPLETE_GOOGLE_API_PHONEME_TRANSFORMATION = [],
    TRANSFORM_TEXT_INTO_PHONEMES = [
        ArpabetPhonemeEvent
    ],
