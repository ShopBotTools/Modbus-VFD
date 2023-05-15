## Make a function for reading the running data from the VFD and create table that refreshes with the live data

def read_VFD():
	
	## Import the related modules / libraries
	import minimalmodbus 
	import Modbus_Settings as MB
	from time import sleep
	import os

	## Create reading "instrument" called "readie_boi" and import it's settings from the modbus settings module
	readie_boi = minimalmodbus.Instrument(MB.USB_port,MB.mb_address )	
	readie_boi.mode = minimalmodbus.MODE_RTU							
	readie_boi.serial.parity = minimalmodbus.serial.PARITY_NONE			
	readie_boi.serial.baudrate = MB.baudrate							
	readie_boi.serial.bytesize = MB.bytesize							
	readie_boi.serial.stopbits = MB.stopbits 							
	readie_boi.serial.timeout  = MB.timeout								
	readie_boi.clear_buffers_before_call = MB.clear_buffers_before_call
	readie_boi.clear_buffers_after_call  = MB.clear_buffers_after_call


	## Set a while loop with a try / except statement so it can be broken with a keyboard interupt
	while True:
		
			## Poll the VFD and set the returned data as a list called "data"  
		try:
			data =readie_boi.read_registers(MB.frequency_reg, MB.read_length, 3) 
			readie_boi.serial.close()
			
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
			print(f"Frequency      :  {float(hirz/100)}Hz")
			print(f"Current        :  {current/10}A")
			print(f"Output Voltage :  {volt}V")
			print(f"DC Bus Voltage :  {bus}V")
			print(f"Total Power    :  {power/10}kW")
			print(f"Operation Code :  {process}")
			print("------------------------------------------")
			print("---------------------------------------------------------------")
			print("---------------------------------------------------------------")
			print("")
			
			
# 			## Debug section, Uncomment for more details on what is in each register address
			# print("")
			# print("--------------------")
			# print("Debug Section")
			# print("--------------------")
			# print("Data at address: ")
			# i = MB.first_reg
			# for x in data:
			# 	print(f"Data in Address {i}: {x}")
			# 	i += 1
			# print("------------------------------------------")


			# print("")
			# print("Press Ctrl+C to Change Settings Or Exit")
			
			
			## Refresh the command line table
			sleep(5)
			os.system('cls' if os.name == 'nt' else 'clear')
			
		# Break the loop and go back to selection menu with a keyboard interupt
		except KeyboardInterrupt:
			break


