import argparse
from controller import VFDController
import modbus_settings as MB

parser = argparse.ArgumentParser()
parser.add_argument('speed', type=int, nargs='?', default=None)
args = parser.parse_args()

if __name__ == "__main__":
    if MB.COM_PORT is None:
        print("No communication with VFD, check USB connection and COM Port")
    else:
        controller = VFDController(MB.COM_PORT)
        # If a speed argument is specified from the command line,
        # then only adjust the speed
        if args.speed:
            # Convert speed to frequency to pass to set_spindle
            controller.connect(MB.COM_PORT)
            int_speed = int(args.speed)
            controller.set_spindle(int_speed / 60)
        # If a speed argument is not specified, then start the gui
        if args.speed is None:
            try:
                controller.start()
            except KeyboardInterrupt:
                print("CTRL+C detected, exiting")
