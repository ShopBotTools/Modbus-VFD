import re
import serial.tools.list_ports
import minimalmodbus

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

def get_com_port():
    # Get a list of all available ports
    available_ports = list(serial.tools.list_ports.comports())

    pattern = r"ShopBot Controller \((COM\d+)\)"
    for port in available_ports:
        match = re.match(pattern, port.description)
        if match:
            com_port = match.group(1)
            try:
                # Attempt to open a serial connection to the port
                with minimalmodbus.serial.Serial(com_port, BAUDRATE) as serial_port:
                    # Attempt to establish a Modbus connection
                    vfd = minimalmodbus.Instrument(serial_port, MB_ADDRESS)
                    # Perform a simple read operation to test the connection
                    vfd.read_register(0)
                    return com_port
            except minimalmodbus.ModbusException:
                # Handle modbus communication error
                pass

    return None

COM_PORT = get_com_port()
