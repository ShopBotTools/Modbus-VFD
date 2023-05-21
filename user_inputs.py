## Import the related modules / libraries
import minimalmodbus
import Modbus_Settings as MB

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

## Create function for prompting the user to input the desired RPM and returns the value to be given to the VFD frequency address
## Returns the string "NaN" if the user input is not a number
## Returns the string "OL" if the user input is outside the limits of 0-60Hz
def get_user_speed():
    print("")
    print("")
    print("------------------------------------------")
    print("Input Drive Speed")
    print("----------------")	
    print("Hirz between 60 - 120")
    print("------------------------------------------")	
    print("")
    print("Press Ctrl + C to Exit")

    speed_input= input()
    try:
        speed_int = int(float(speed_input)*10)
    except:
        return "NaN"
    else:
        if isinstance(speed_int, int):
            if speed_int >=600 and speed_int <=1200:
                return speed_int
            else:
                return "OL"
        else:
            return "NaN"

def set_user_speed(speed):
    try:
        speed_int = int(float(speed)*10)
    except:
        return "NaN"
    else:
        if isinstance(speed_int, int):
            if speed_int >=600 and speed_int <=1200:
                return speed_int
            else:
                return "OL"
        else:
            return "NaN"


## Send the request to the vfd
def send_to_vfd(register, data, function_code, decimals = 0, signed = False):
    writer.write_register(register, data, decimals, function_code, signed)
    writer.serial.close()








