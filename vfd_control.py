## Import the related modules / libraries
import user_inputs
import minimalmodbus
import Modbus_Settings as MB
import argparse
import threading

## Create writing "instrument" that can perform write operations and import it's settings from the modbus settings module
writer = minimalmodbus.Instrument(MB.USB_port, MB.mb_address)
writer.mode = minimalmodbus.MODE_RTU
writer.serial.parity = minimalmodbus.serial.PARITY_NONE
writer.serial.baudrate = MB.baudrate
writer.serial.bytesize = MB.bytesize
writer.serial.stopbits = MB.stopbits
writer.serial.timeout  = MB.timeout
writer.clear_buffers_before_each_transaction = MB.clear_buffers_before_call
writer.close_port_after_each_call = MB.clear_buffers_after_call
writer.debug = MB.debug

# Create a lock for synchronization
lock = threading.Lock()

speed_set = False

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=int,  help = "Change the spindle speed, 60-120 currently")
args = parser.parse_args()

if args.speed:
    speed_package = user_inputs.set_user_speed(args.speed)
    if speed_package != "NaN" and speed_package != "OL":
        speed_set = True

## Send the request to the vfd
def send_to_vfd(register, data, function_code, decimals = 0, signed = False):
    with lock:
        writer.write_register(register, data, decimals, function_code, signed)
        writer.serial.close()

# # If the speed has been set correctly then pass on the speed package as
# # well as the register position to the function to send to the VFD
if speed_set:
    print("Attempting unlock drive")
    send_to_vfd(MB.unlock_drive, MB.password, MB.WRITE_SINGLE_REGISTER)
    print("Attempting unlock parameters")
    send_to_vfd(MB.unlock_parameters, MB.password, MB.WRITE_SINGLE_REGISTER)
    print("Attempting set frequency")
    send_to_vfd(MB.set_frequency, speed_package, MB.WRITE_SINGLE_REGISTER)

