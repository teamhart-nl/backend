from ..helpers.SingletonHelper import Singleton
from ..models.EventTypeEnum import EventType


class Dispatcher(metaclass=Singleton):
    """
    The dispatcher links events to their corresponding triggers and fires them.
    """

    def handle(self, data):
        """
        Based on the event type of the parsed data, this function triggers the corresponding events.
        :param data:    the parsed data.
        # TODO data needs to be of some abstract datatype (still have to figure out what)
        """

        # Log arrival of data TODO extent when datatype is determined
        print("Received dispatcher data of type " + type(data))

        # Loop over all events that need to be triggered for the EventType of the data
        for event in EventType[data.eventType]:
            data = event.handle(data.eventType, data)
