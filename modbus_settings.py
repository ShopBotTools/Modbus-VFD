# Set the Modbus paramaters in here for both reading and writing to the VFD
# General Modbus Settings
import configparser
import os
import sys

config = configparser.ConfigParser()
executable_dir = os.path.dirname(sys.argv[0])
config_file = 'config.ini'
config_path = os.path.join(executable_dir, config_file)
config.read(config_path)
# Use the value of the 'COM' key in the 'Serial' section of the config file
com_port = config.get('Serial', 'COM')

COM_PORT = com_port
MB_ADDRESS = 3                          # Station Address
BAUDRATE = 9600                         # BAUDRATE
BYTESIZE = 8                            # Number of data bits to be requested
STOPBITS = 1                            # Number of stop bits
TIMEOUT = 0.25                           # TIMEOUT time in seconds
CLEAR_BUFFERS_BEFORE_CALL = True        # Good practice clean up
CLEAR_BUFFERS_AFTER_CALL  = True        # Good practice clean up
DEBUG = False

# P194
PASSWORD = 0

# Registers
COMMAND_DRIVE     = 1
READ_FREQUENCY    = 24
SET_FREQUENCY     = 44
UNLOCK_DRIVE      = 48
UNLOCK_PARAMETERS = 49

# Bits
COMMAND_DRIVE_SECURITY_BIT = 2

# Define Modbus function codes
READ_REGISTER         = 3
WRITE_SINGLE_REGISTER = 6

## Read Settings
READ_LENGTH = 6                # Number of adresses to read when Polling the VFD for data
