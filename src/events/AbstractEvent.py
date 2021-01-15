from abc import ABC, abstractmethod

from src.models.EventTypeEnum import EventType
from src.models.request_data import AbstractRequest


class AbstractEvent(ABC):
    """
    Abstract class that every event should extend on.
    """

    @abstractmethod
    def handle(self, request_data: AbstractRequest):
        """
        Handles the event based on the given data.
        :param event_type:      General event type that is being processed.
        :param request_data:    Data that has to be handled by the event
        """
        pass

    @staticmethod
    @abstractmethod
    def get_priority() -> int:
        pass

    @staticmethod
    @abstractmethod
    def get_compatible_events() -> [EventType]:
        pass
