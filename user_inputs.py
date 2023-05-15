## Import the related modules / libraries
import minimalmodbus
import Modbus_Settings as MB

	## Create reading "instrument" called "turnie_boi" and import it's settings from the modbus settings module

turny_boi = minimalmodbus.Instrument(MB.USB_port, MB.mb_address)
turny_boi.mode = minimalmodbus.MODE_RTU
turny_boi.serial.parity = minimalmodbus.serial.PARITY_NONE
turny_boi.serial.baudrate = MB.baudrate
turny_boi.serial.bytesize = MB.bytesize
turny_boi.serial.stopbits = MB.stopbits
turny_boi.serial.timeout  = MB.timeout
turny_boi.clear_buffers_before_each_transaction = MB.clear_buffers_before_call
turny_boi.close_port_after_each_call = MB.clear_buffers_after_call 

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
		speed_int = int(float(speed_input)*100)
	except:
		return "NaN"
	else:
		if isinstance(speed_int, int):
			if speed_int >=600 and speed_int <=12000:
				return speed_int
			else:
				return "OL"
		else:
			return "NaN"



## Send the request to the vfd
def send_to_vfd(register, data, function_code, decimals = 0, signed = False):
	turny_boi.write_register(register, data, decimals, function_code, signed)
	turny_boi.serial.close()








