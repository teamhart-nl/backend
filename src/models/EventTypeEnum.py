from enum import Enum


class EventType(Enum):
    """
    Enum for all event types.
    """

    COMPLETE_GOOGLE_API_PHONEME_TRANSFORMATION = 1,
    TRANSFORM_TEXT_INTO_PHONEMES = 2

    @staticmethod
    def get_all_event_types():
        # TODO type this
        return list(map(lambda c: c, EventType))
