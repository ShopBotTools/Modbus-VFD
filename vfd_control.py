## Import the related modules / libraries
import minimalmodbus 
import user_inputs
import Modbus_Settings as MB
import stat_display as stat
from time import sleep 
import os
import sys


## Set some flags we use to step through the data input and parsing
#drive_set = False
unlocked = False
speed_set = False
# drive_package = 0
speed_package = 0


## Main loop of the program

while True:
	# if unlocked == False:
	# 	user_inputs.send_to_vfd(MB.unlock_reg, MB.password, MB.WRITE_SINGLE_REGISTER)
	# # If the drive mode has been set but the speed has not yet been set the get the speed setting from user and assign it to "speed_package"
	# if speed_set == False:
	# 	speed_package = user_inputs.get_user_speed()
		
	# 	# If the functinon returns any of the various errors, tell the user what the error was
	# 	if speed_package == "NaN":
	# 		print("")
	# 		print("Speed entered is not a number")
	# 	elif speed_package == "OL":
	# 		print("")
	# 		print("Speed Under/Over Limits")
			
	# 	# If there was no error then set the flag "speed_set" true and tell the user what it is set to 
	# 	else:
	# 		print("")
	# 		print(f"Speed set to {speed_package}")
	# 		speed_set = True
		
	# # If the dirve mode and the speed have both been set correctly then pass on the drive and speed packages as well as the register position to the funcion to send to the VFD	
	# if speed_set == True:
	# 	user_inputs.send_to_vfd(MB.unlock_reg, speed_package)
	
	# If both drive and speed are set and the data has been sent to the VFD, then clear the screen and call the snazzy info display function
	# if speed_set:
	os.system('cls' if os.name == 'nt' else 'clear')
	stat.read_VFD()
	# drive_set = False
	speed_set = False
	os.system('cls' if os.name == 'nt' else 'clear')
