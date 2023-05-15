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
	# If both drive and speed are set and the data has been sent to the VFD, then clear the screen and call the snazzy info display function
	# if speed_set:
	os.system('cls' if os.name == 'nt' else 'clear')
	stat.read_VFD()
	# drive_set = False
	speed_set = False
	os.system('cls' if os.name == 'nt' else 'clear')
