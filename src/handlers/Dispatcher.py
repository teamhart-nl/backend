import pkgutil
from typing import Dict, List
import os, importlib

from src.helpers.Logger import Logger
from src import events
from src.events import AbstractEvent as AE
from src.events.AbstractEvent import AbstractEvent
from src.helpers.SingletonHelper import Singleton
from src.models.EventTypeEnum import EventType
from src.models.request_data import AbstractRequest


class Dispatcher(metaclass=Singleton):
    """
    The dispatcher links events to their corresponding triggers and fires them. Extends on Singleton helper, thus there
    exists only one dispatcher object at all times.
    """

    """event_type_map maps every event type to a list of Events. List is initialized upon first creation of the
    Dispatcher."""
    event_type_map: Dict[EventType, List]

    def __init__(self):
        # Initialize event_type_map
        self.event_type_map = {}

        # For each event_type, add an instance to the dictionary
        for event_type in EventType:
            self.event_type_map[event_type.name] = []

        # Import all events in the events module
        for (module_loader, name, ispk) in pkgutil.iter_modules([os.path.dirname(AE.__file__)]):
            importlib.import_module('.' + name, events.__name__)

        # Loop through all events that extend AbstractEvent
        for event_class in AbstractEvent.__subclasses__():
            # Check which event_types they belong to and add them to the lists in the event_type_map
            for event_type in event_class.get_compatible_events():
                self.event_type_map.get(event_type.name).append(event_class)

        # Sort the lists (values) in the event_type_map on priority (reversed, thus high priority first)
        for event_list in self.event_type_map.values():
            event_list.sort(key=lambda x: x.get_priority(), reverse=True)

        Logger.log_info("Dispatcher has been initialized.")

    def handle(self, data: AbstractRequest) -> None:
        """
        Based on the event type of the parsed data, this function triggers the corresponding events.
        :param data:    the parsed data.
        """

        # Log arrival of data
        Logger.log_info("Dispatcher.handle: Received dispatcher data of type " + data.get_event_type().name)

        # Loop over all events that need to be triggered for the EventType of the data
        for event in self.event_type_map[data.get_event_type().name]:
            try:
                # Try to handle the event
                data = event().handle(data)
            except Exception as e:
                # Catch and report exception
                Logger.log_warning("FATAL ERROR! Stopping event execution")
                Logger.log_warning("Dispatcher.handle: Stopped event was of type " + event.__class__.__name__)
                Logger.log_warning("Complete error: " + str(e))
                return

