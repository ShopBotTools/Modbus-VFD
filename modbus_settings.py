# Set the Modbus paramaters in here for both reading and writing to the VFD
# General Modbus Settings
import serial
import serial.tools.list_ports
import re
import minimalmodbus
import threading

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

lock = threading.Lock()

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

def is_modbus_vfd_controller(com_port):
    try:
        vfd = minimalmodbus.Instrument(com_port, MB_ADDRESS)
        vfd.mode = minimalmodbus.MODE_RTU
        vfd.serial.parity = minimalmodbus.serial.PARITY_NONE
        vfd.serial.baudrate = BAUDRATE
        vfd.serial.bytesize = BYTESIZE
        vfd.serial.stopbits = STOPBITS
        vfd.serial.timeout = TIMEOUT
        vfd.clear_buffers_before_each_transaction = CLEAR_BUFFERS_BEFORE_CALL
        vfd.close_port_after_each_call = CLEAR_BUFFERS_AFTER_CALL
        vfd.debug = DEBUG
    except minimalmodbus.ModbusException as e:
        # Handle modbus communication error
        print("Modbus Exception:", e)
    except PermissionError as e:
        # Handle permission error
        print("Permission Error:", e)
    except Exception as e:
        # Handle other exceptions
        print("Exception:", e)
    with lock:
        try:
            # Read data from the device
            data = vfd.read_registers(READ_FREQUENCY, READ_LENGTH, READ_REGISTER)
            return data

        except minimalmodbus.ModbusException as e:
            # Handle modbus communication error
            print("Modbus Exception:", e)
        except PermissionError as e:
            # Handle permission error
            print("Permission Error:", e)
        except Exception as e:
            # Handle other exceptions
            print("Exception:", e)

COM_PORT = get_com_port()