from src.helpers.Logger import Logger
from src.helpers.SingletonHelper import Singleton

from typing import Dict, Any, List

import serial
import serial.tools.list_ports

'''
represents the current connection with an arduino
'''
class ArduinoConnection(metaclass=Singleton):

    #maps coord in the phoneme pattern jsons to the id of the motor from specific arduino
    self.mapping : Dict[int, int]

    #whether backend in debug (so no connected arduino)
    self.debug : bool

    #baudrate for connected arduino
    self.baudrate : int

    #list of serials of known arduinos (should include current connected arduino)
    self.serials : List[str]

    '''
    establish connection with arduino

    param config_file: JSON dictionary with arduino specific settings
    '''
    def __init__(self, config_json : Dict[str, Any]):
        #parse config settings for arduino
        self.parse_config_JSON(config_file) 

        #set found device
        if not self.debug:
            self.device = serial.Serial(self.find_arduino_port(), baudrate=self.baudrate)

    '''
    parse the config json file 

    param config_file: JSON dictionary with arduino specific settings
    '''
    def parse_config_JSON(self, config_file):
        #get mapping of motor coord to id
        self.mapping = {}
        for pair in config['mapping']:
            self.mapping[pair['coord']] = pair['coord']

        # serials of known arduinos
        self.serials = config['serials']
        #baudrate that is used in arduino
        self.baudrate = config['baudrate']
        #debug mode or not
        self.debug = (config['mode'] == 'debug')

    '''
    finds the first port with an arduino connected with known serial number
    '''
    def find_arduino_port(self) ->  Any:
        for port_info in serial.tools.list_ports.comports():
            if port_info.serial_number in self.serials:
                return port_info.device
        else:
            raise IOError('Could not find a known Arduino, is it plugged in and set as known serial number?')
        

    '''
    send pattern for a phoneme to arduino
    '''
    def send_pattern(self, pattern_JSON: Dict[str, Any]):
        for i in range(len(pattern_JSON['pattern'])):
            for j in range(len(command['pins'])):
                # translate coordinate of pin to ids of pins of arduino
                pattern_JSON['pattern'][i]['pins'][j]['pin'] = self.mapping[pattern_JSON['pattern'][i]['pins'][j]['pin']] 
        
        self.query(json.dumps(pattern_JSON, indent=4, sort_keys=True))

    '''
    generic query
    '''
    def query(self, message : str) -> str:
        # Send message to Arduino.
        if not self.debug:
            self.device.write(message.encode('ascii'))

            # Make sure the Arduino always gives an output, otherwise Python will wait forever.
            line = self.device.readline().decode('ascii').strip()
        else:
            Logger.log_info("ArduinoConnection.query: A would have now arrived at the arduino")
            line = ""
        return line