import argparse
from controller import VFDController
import modbus_settings as MB

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=int,  help = "Change the spindle speed, 7200-18000 currently")
parser.add_argument("-f", "--frequency", type=int,  help = "Change the frequency, 120-300 currently")
args = parser.parse_args()

if __name__ == "__main__":
        controller = VFDController(MB.COM_PORT)
        if args.speed:
            # Convert speed to frequency to pass to set_spindle
            controller.connect(MB.COM_PORT)
            int_speed = int(args.speed)
            controller.set_spindle(int_speed / 60)
        if args.frequency:
            controller.connect(MB.COM_PORT)
            int_frequency = int(args.frequency)
            controller.set_frequency(int_frequency)
        elif not args:
            try:
                controller.start()
            except KeyboardInterrupt:
                print("CTRL+C detected, exiting")
