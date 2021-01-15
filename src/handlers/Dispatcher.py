import pkgutil
from typing import Dict, List
import os, importlib
from glob import glob


from src import events
from src.events import AbstractEvent as AE
from src.events.AbstractEvent import AbstractEvent
from src.helpers.SingletonHelper import Singleton
from src.models.EventTypeEnum import EventType
from src.models.request_data import AbstractRequest


class Dispatcher(metaclass=Singleton):
    """
    The dispatcher links events to their corresponding triggers and fires them.
    """

    event_type_map: Dict[EventType, List]

    def __init__(self):
        self.event_type_map = {}

        for event_type in EventType.get_all_event_types():
            self.event_type_map[event_type.name] = []

        for (module_loader, name, ispk) in pkgutil.iter_modules([os.path.dirname(AE.__file__)]):
            importlib.import_module('.' + name, events.__name__)

        for event_class in AbstractEvent.__subclasses__():
            for event_type in event_class.get_compatible_events():
                self.event_type_map.get(event_type.name).append(event_class)

        for l in self.event_type_map.values():
            l.sort(key=lambda x: x.get_priority())

    def handle(self, data: AbstractRequest) -> None:
        """
        Based on the event type of the parsed data, this function triggers the corresponding events.
        :param data:    the parsed data.
        """

        # Log arrival of data
        print("Received dispatcher data of type " + data.get_event_type().name)

        # Loop over all events that need to be triggered for the EventType of the data
        for event in self.event_type_map[data.get_event_type().name]:
            data = event().handle(data)
