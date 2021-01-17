from abc import ABC, abstractmethod

from src.models.EventTypeEnum import EventType
from src.models.request_data import AbstractRequest


class AbstractEvent(ABC):
    """
    Abstract class that every event should extend on.
    """

    @abstractmethod
    def handle(self, request_data: AbstractRequest) -> AbstractRequest:
        """
        Handles the event based on the given data.
        :param request_data:    Data that has to be handled by the event
        """
        pass

    @staticmethod
    @abstractmethod
    def get_priority() -> int:
        """
        Returns the priority of the event (higher means more priority and thus executed earlier)
        """
        pass

    @staticmethod
    @abstractmethod
    def get_compatible_events() -> [EventType]:
        """
        Returns a list of all EventTypes that this event is part of.
        """
        pass
