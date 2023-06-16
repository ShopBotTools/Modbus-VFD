# Set the Modbus paramaters in here for both reading and writing to the VFD
# General Modbus Settings
import serial
import serial.tools.list_ports
import re
from pymodbus.client.sync import ModbusSerialClient

def is_modbus_vfd_controller(com_port):
    # Create a Modbus client
    client = ModbusSerialClient(method='rtu', port=com_port, baudrate=9600)

    try:
        # Connect to the Modbus device
        if client.connect():
            # Send a simple read request to address 0
            response = client.read_holding_registers(0, 1, unit=1)
            if response.isError():
                # Modbus read request was unsuccessful
                return False
            else:
                # Modbus read request was successful
                return True
        else:
            # Failed to connect to the Modbus device
            return False
    finally:
        # Close the Modbus client
        client.close()

def get_com_port():
    # Get a list of all available ports
    available_ports = list(serial.tools.list_ports.comports())

    pattern = r"ShopBot Controller \((COM\d+)\)"
    for port in available_ports:
        match = re.match(pattern, port.description)
        if match:
            com_port = match.group(1)
            # Check if it is the correct port by sending a modbus read request
            if is_modbus_vfd_controller(com_port):
                return com_port

    return None

MB_ADDRESS = 3                          # Station Address
COM_PORT = get_com_port()
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
