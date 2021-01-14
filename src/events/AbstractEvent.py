from abc import ABC, abstractmethod

from src.models.request_data import AbstractRequest


class AbstractEvent(ABC):
    """
    Abstract class that every event should extend on.
    """

    @abstractmethod
    def handle(self, request_data: AbstractRequest):
        """
        Handles the event based on the given data.
        TODO determine if we need an object to pass around of some 'processed data' type or something like that
        :param event_type:      General event type that is being processed.
        :param request_data:    Data that has to be handled by the event
        """
        pass
