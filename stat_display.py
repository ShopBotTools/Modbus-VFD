## Make a function for reading the running data from the VFD and create table that refreshes with the live data

def read_VFD():
	
	## Import the related modules / libraries
	import minimalmodbus 
	import Modbus_Settings as MB
	from time import sleep
	import os

	## Create reading "instrument" called "reader" and import it's settings from the modbus settings module
	reader = minimalmodbus.Instrument(MB.USB_port,MB.mb_address )
	reader.mode = minimalmodbus.MODE_RTU
	reader.serial.parity = minimalmodbus.serial.PARITY_NONE
	reader.serial.baudrate = MB.baudrate
	reader.serial.bytesize = MB.bytesize
	reader.serial.stopbits = MB.stopbits
	reader.serial.timeout  = MB.timeout
	reader.clear_buffers_before_each_transaction = MB.clear_buffers_before_call
	reader.close_port_after_each_call  = MB.clear_buffers_after_call
	reader.debug = MB.debug


	## Set a while loop with a try / except statement so it can be broken with a keyboard interupt
	while True:
		
			## Poll the VFD and set the returned data as a list called "data"
		try:
			data = reader.read_registers(MB.read_frequency, MB.read_length, MB.READ_REGISTER)
			reader.serial.close()
			
			## Split out the list into individual variables
			current = data[0]
			hirz = data[1]
			volt = data[2]
			bus = data[3]
			power = data[4]
			process = data[5]

# 			## Print out all the data
			print("")
			print("------------------------------------------")
			print("VFD Viewer")
			print("------------------------------------------")
			print(f"Current        :  {current/10}A")
			print(f"Frequency      :  {float(hirz/100)}Hz")
			print(f"Output Voltage :  {volt}V")
			print(f"DC Bus Voltage :  {bus}V")
			print(f"Total Power    :  {power/10}kW")
			print(f"Operation Code :  {process}")
			print("------------------------------------------")
			print("---------------------------------------------------------------")
			print("---------------------------------------------------------------")
			# print(f"password: {data2}")

# 			## Debug section, Uncomment for more details on what is in each register address
			print("")
			print("--------------------")
			print("Debug Section")
			print("--------------------")
			i = MB.read_frequency
			for x in data:
				print(f"Data in Address {i}: {x}")
				i += 1
			print("------------------------------------------")
			print("")
			print("Press Ctrl+C to Change Settings Or Exit")


			## Refresh the command line table
			sleep(5)
			os.system('cls' if os.name == 'nt' else 'clear')

		# Break the loop and go back to selection menu with a keyboard interupt
		except KeyboardInterrupt:
			break


