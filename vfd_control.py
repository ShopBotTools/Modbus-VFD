## Import the related modules / libraries
import user_inputs
import Modbus_Settings as MB
import stat_display as stat
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=int,  help = "Change the spindle speed, 60-120 currently")
args = parser.parse_args()

## Set some flags we use to step through the data input and parsing
unlocked = False
speed_set = False
speed_package = 0


## Main loop of the program
while True:
    if speed_set == False:
        if args.speed:
            speed_package = user_inputs.set_user_speed(args.speed)

    # # If the speed has been set correctly then pass on the speed package as
    # # well as the register position to the function to send to the VFD
    if speed_set == True:
        if unlocked == False:
            print("Attempting unlock drive")
            user_inputs.send_to_vfd(MB.unlock_drive, MB.password, MB.WRITE_SINGLE_REGISTER)
            print("Attempting unlock parameters")
            user_inputs.send_to_vfd(MB.unlock_parameters, MB.password, MB.WRITE_SINGLE_REGISTER)
            unlocked = True
        print("Attempting set frequency")
        user_inputs.send_to_vfd(MB.set_frequency, speed_package, MB.WRITE_SINGLE_REGISTER)

