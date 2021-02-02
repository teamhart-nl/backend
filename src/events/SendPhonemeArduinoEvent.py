
from src.models.EventTypeEnum import EventType
from src.events.AbstractEvent import AbstractEvent
from src.helpers.Logger import Logger
from src.models.request_data.AbstractRequest import AbstractRequest
from src.modules.ArduinoConnection import ArduinoConnection


class SendPhonemeArduinoEvent(AbstractEvent):

    PRIORITY: int = 90

    def __init__(self):
        pass

    def handle(self, request_data : AbstractRequest):
        Logger.log_info("Sending the pattern for {} to the arduino.".format(request_data.phoneme))
        ArduinoConnection.send_pattern(request_data.phoneme_pattern)
        Logger.log_info("Sending of pattern for {} completed.".format(request_data.phoneme))

        return request_data

    @staticmethod
    def get_priority() -> int:
        return SendPhonemeArduinoEvent.PRIORITY

    @staticmethod
    def get_compatible_events() -> [EventType]:
        return [
            EventType.TRANSLATE_USING_GOOGLE_API,
            EventType.SEND_PHONEME_TO_MICROCONTROLLER
        ]