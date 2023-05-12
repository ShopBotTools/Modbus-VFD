## Set the Modbus paramaters in here for both reading and writing to the VFD


## General Modbus Settings

mb_address = 1							# Station Address
USB_port = "COM3"				# Location of USB to RS485 converter
baudrate = 9600							# BaudRate
bytesize = 8							# Number of data bits to be requested
stopbits = 1							# Number of stop bits
timeout = 0.5							# Timeout time in seconds
clear_buffers_before_call = True		# Good practice clean up
clear_buffers_after_call  = True		# Good practice clean up

##
password = 27

## Write Settings
unlock_reg = 48
frequency_reg = 24

# Define Modbus function codes
WRITE_SINGLE_REGISTER = 6

## Read Settings
#reading_offset = 40009					# Offset for reading the state of the VFD
read_length = 6							# Number of adresses to read when Polling the VFD for data
