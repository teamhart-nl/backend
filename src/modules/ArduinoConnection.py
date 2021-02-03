from src.helpers.Logger import Logger
from src.helpers.SingletonHelper import SingletonArduino

from typing import Dict, Any, List

import serial
import serial.tools.list_ports

import os
import json

'''
represents the current connection with an arduino
'''
class ArduinoConnection(metaclass=SingletonArduino):

    #configured
    configured : bool = False

    #maps coord in the phoneme pattern jsons to the id of the motor from specific arduino
    mapping : Dict[int, int]

    #whether backend in debug (so no connected arduino)
    debug : bool

    #baudrate for connected arduino
    baudrate : int

    #list of serials of known arduinos (should include current connected arduino)
    serials : List[str]

    '''
    establish connection with arduino

    param config_file: JSON dictionary with arduino specific settings
    '''
    def __init__(self):
        pass
        
    def connect_with_config(self, fp_json : str):
        with open(fp_json, 'r') as f:
                json_config = json.load(f)

        self.parse_config_JSON(json_config) 

        #set found device
        if not self.debug:
            self.device = serial.Serial(self.find_arduino_port(), baudrate=self.baudrate)
        
        print("reached this")
        self.configured = True

    '''
    parse the config json file 

    param config_file: JSON dictionary with arduino specific settings
    '''
    def parse_config_JSON(self, config):
        #get mapping of motor coord to id
        self.mapping = {}
        for pair in config['mapping']:
            self.mapping[pair['coord']] = pair['coord']

        # serials of known arduinos
        self.serials = config['serial_numbers']
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
        #check if configured
        if not self.configured:
            raise Exception("Illegal state, attempt to send pattern to arduino without it being configured")

        #map from coords to ids
        for i in range(len(pattern_JSON['pattern'])):
            for j in range(len(pattern_JSON['pattern'][i]['pins'])):
                # translate coordinate of pin to ids of pins of arduino
                pattern_JSON['pattern'][i]['pins'][j]['pin'] = self.mapping[pattern_JSON['pattern'][i]['pins'][j]['pin']] 
        
        #send to arduino
        self.query(json.dumps(pattern_JSON, indent=4, sort_keys=True))

    '''
    generic query
    '''
    def query(self, message : str) -> str:
        #check if configured
        if not self.configured:
            raise Exception("Illegal state, attempt to send pattern to arduino without it being configured")

        # Send message to Arduino.
        if not self.debug:
            self.device.write(message.encode('ascii'))

            # Make sure the Arduino always gives an output, otherwise Python will wait forever.
            line = self.device.readline().decode('ascii').strip()
        else:
            Logger.log_info("ArduinoConnection.query: A would have now arrived at the arduino")
            line = ""
        return line
    