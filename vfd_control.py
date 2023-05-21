## Import the related modules / libraries
import user_inputs
import Modbus_Settings as MB
import argparse
import threading

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

# # If the speed has been set correctly then pass on the speed package as
# # well as the register position to the function to send to the VFD
if speed_set:
        print("Attempting unlock drive")
        user_inputs.send_to_vfd(MB.unlock_drive, MB.password, MB.WRITE_SINGLE_REGISTER)
        print("Attempting unlock parameters")
        user_inputs.send_to_vfd(MB.unlock_parameters, MB.password, MB.WRITE_SINGLE_REGISTER)
        print("Attempting set frequency")
        user_inputs.send_to_vfd(MB.set_frequency, speed_package, MB.WRITE_SINGLE_REGISTER)

