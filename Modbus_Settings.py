## Set the Modbus paramaters in here for both reading and writing to the VFD

## General Modbus Settings

mb_address = 3							# Station Address
USB_port = "COM4"				        # Location of USB to RS485 converter
baudrate = 9600							# BaudRate
bytesize = 8							# Number of data bits to be requested
stopbits = 1							# Number of stop bits
timeout = 0.5							# Timeout time in seconds
clear_buffers_before_call = True		# Good practice clean up
clear_buffers_after_call  = True		# Good practice clean up
debug = True

## P194
password = 0

## Registers
read_frequency = 24
set_frequency = 44
unlock_drive = 48
unlock_parameters = 49

# Define Modbus function codes
READ_REGISTER = 3
WRITE_SINGLE_REGISTER = 6

## Read Settings
read_length = 6			                # Number of adresses to read when Polling the VFD for data
