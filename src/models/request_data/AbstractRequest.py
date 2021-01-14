from abc import ABC, abstractmethod

# from src.models.EventTypeEnum import EventType


class AbstractRequest(ABC):
    """
    AbstractEventRequestData is an abstract class for all processing requests that will eventually be send to the
    dispatcher.
    """

    @abstractmethod
    def get_event_type(self):
        """
        In concrete classes, this method should return the event type based on the data provided in the request, which
        is then part of this object.
        """
        pass
