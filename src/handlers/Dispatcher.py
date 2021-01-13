from src.helpers.SingletonHelper import Singleton
from src.models import AbstractEventRequestData


class Dispatcher(metaclass=Singleton):
    """
    The dispatcher links events to their corresponding triggers and fires them.
    """

    def handle(self, data: AbstractEventRequestData):
        """
        Based on the event type of the parsed data, this function triggers the corresponding events.
        :param data:    the parsed data.
        """

        # Log arrival of data
        print("Received dispatcher data of type " + data.get_event_type().name)

        # Loop over all events that need to be triggered for the EventType of the data
        for event in data.get_event_type().value:
            data = event.handle(data)
