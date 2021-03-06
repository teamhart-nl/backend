from src.helpers.Logger import Logger
from src.helpers.SingletonHelper import Singleton

from typing import Dict, Any, List

import serial
import serial.tools.list_ports

import json
import copy


class ArduinoConnection(metaclass=Singleton):
    """
    Represents the connection with an Arduino
    """

    # configured
    configured: bool = False

    # maps coord in the phoneme pattern jsons to the id of the motor from specific arduino
    mapping: Dict[int, int]

    # whether backend in debug (so no connected arduino)
    debug: bool

    # baudrate for connected arduino
    baudrate: int

    # list of serials of known Arduino's (should include current connected arduino)
    serials: List[str]

    def __init__(self):
        pass

    def connect_with_config(self, fp_json: str):
        """
        Establish connection with arduino

        param fp_json: filepath to JSON with arduino specific settings
        """

        # load json file
        with open(fp_json, 'r') as f:
            json_config = json.load(f)

        # parse data from config json
        self.parse_config_JSON(json_config)

        # set found device if not in backend-debug mode
        if not self.debug:
            try:
                port = self.find_arduino_port()
                Logger.log_info("Connecting to port: " + port)
                self.device = serial.Serial(port, baudrate=self.baudrate, timeout=1)
                Logger.log_info("Connection is open: " + str(self.device.is_open))
            except Exception as e:
                Logger.log_warning("Arduino connection NOT successfully created! " + str(e))
                self.configured = False
                return

        self.configured = True

    def parse_config_JSON(self, config):
        """
        parse the config json file

        param config_file: JSON dictionary with arduino specific settings
        """

        # get mapping of motor coord to id
        self.mapping = {}
        for pair in config['mapping']:
            self.mapping[pair['coord']] = pair['id']

        # serials of known arduinos
        self.serials = config['serial_numbers']

        # baudrate that is used in arduino
        self.baudrate = config['baudrate']

        # debug mode or not
        self.debug = (config['mode'] == 'debug')

    def find_arduino_port(self) -> Any:
        """
        finds the first port with an arduino connected with known serial number
        """

        # run through ports to find matching serial-number
        for port_info in serial.tools.list_ports.comports():

            # if serial number of connection port is familiar
            if port_info.serial_number in self.serials:
                return port_info.device
        else:
            raise IOError('ArduinoConnection.find_arduino_port: Could not find a known Arduino, '
                          'is it plugged in and set as known serial number?')

    def send_pattern(self, pattern_JSON: Dict[str, Any]):
        """
        Send a phoneme pattern to arduino
        """

        # check if connection is configured
        if not self.configured:
            raise Exception("ArduinoConnection.send_pattern: Illegal state, "
                            "attempt to send pattern to arduino without it being configured")

        # deep copy json as to prevent overwriting mapping
        mapped_pattern_JSON = copy.deepcopy(pattern_JSON)

        # map from coords to ids
        for i in range(len(mapped_pattern_JSON['pattern'])):
            for j in range(len(mapped_pattern_JSON['pattern'][i]['pins'])):
                # translate coordinate of pin (in pattern json) to ids of pins of arduino (in config json)
                mapped_pattern_JSON['pattern'][i]['pins'][j]['pin'] = self.mapping[
                    mapped_pattern_JSON['pattern'][i]['pins'][j]['pin']]

        # send to arduino
        self.query(json.dumps(mapped_pattern_JSON, indent=4, sort_keys=True))

    def query(self, message: str) -> str:
        """
        Generic string query to the arduino
        """

        # check if configured
        if not self.configured:
            raise Exception("ArduinoConnection.query: Illegal state, "
                            "attempt to send pattern to arduino without it being configured")

        # Send message to Arduino.
        if not self.debug:
            try:

                self.device.write(message.encode('ascii'))

                # Make sure the Arduino always gives an output, otherwise Python will wait forever.
                arduino_log = self.device.readline().strip().decode('ascii', errors="ignore")
                Logger.log_info("Arduino says: " + arduino_log)
            except Exception as e:
                Logger.log_warning("ArduinoConnection.query: error occurred during sending. Complete error: " + str(e))
                arduino_log = "ArduinoConnection.query: Arduino could not be obtained."

        else:
            Logger.log_info("ArduinoConnection.query: A query would have now arrived at the arduino")
            arduino_log = "Debug log"

        return arduino_log
