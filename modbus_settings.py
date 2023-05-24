# Set the Modbus paramaters in here for both reading and writing to the VFD
# General Modbus Settings

MB_ADDRESS = 3                          # Station Address
USB_PORT = "COM4"                       # Location of USB to RS485 converter
BAUDRATE = 9600                         # BAUDRATE
BYTESIZE = 8                            # Number of data bits to be requested
STOPBITS = 1                            # Number of stop bits
TIMEOUT = 0.5                           # TIMEOUT time in seconds
CLEAR_BUFFERS_BEFORE_CALL = True        # Good practice clean up
CLEAR_BUFFERS_AFTER_CALL  = True        # Good practice clean up
DEBUG = True

## P194
PASSWORD = 0

## Registers
READ_FREQUENCY    = 24
SET_FREQUENCY     = 44
UNLOCK_DRIVE      = 48
UNLOCK_PARAMETERS = 49

# Define Modbus function codes
READ_REGISTER         = 3
WRITE_SINGLE_REGISTER = 6

## Read Settings
READ_LENGTH = 6                # Number of adresses to read when Polling the VFD for data