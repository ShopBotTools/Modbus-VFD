## Import the related modules / libraries
import minimalmodbus 
import user_inputs
import Modbus_Settings as MB
import stat_display as stat
from time import sleep 
import os
import sys


## Set some flags we use to step through the data input and parsing
unlocked = False
speed_set = False
speed_package = 0


## Main loop of the program
while True:
	if unlocked == False:
		user_inputs.send_to_vfd(MB.unlock_parameters, MB.password, MB.WRITE_SINGLE_REGISTER)
		unlocked = True
	if speed_set == False:
		speed_package = user_inputs.get_user_speed()
		# If the function returns any of the various errors, tell the user what the error was
		if speed_package == "NaN":
			print("")
			print("Speed entered is not a number")
		elif speed_package == "OL":
			print("")
			print("Speed Under/Over Limits")
			
		# If there was no error then set the flag "speed_set" true and tell the user what it is set to 
		else:
			print("")
			print(f"Speed set to {speed_package}")
			speed_set = True

	# # If the speed has been set correctly then pass on the speed package as
	# # well as the register position to the function to send to the VFD
	if speed_set == True:
		user_inputs.send_to_vfd(MB.set_frequency, speed_package, MB.WRITE_SINGLE_REGISTER)
	# If speed is set and the data has been sent to the VFD, then clear the screen and call the info display function
	if speed_set:
		os.system('cls' if os.name == 'nt' else 'clear')
		stat.read_VFD()
		speed_set = False
		unlocked = False
		os.system('cls' if os.name == 'nt' else 'clear')
