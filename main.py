import argparse
from controller import VFDController
import modbus_settings as MB

parser = argparse.ArgumentParser()
parser.add_argument('speed', type=int, nargs='?', default=None)
args = parser.parse_args()

if __name__ == "__main__":
    controller = VFDController(MB.COM_PORT)
    if args.speed:
        # Convert speed to frequency to pass to set_spindle
        controller.connect(MB.COM_PORT)
        int_speed = int(args.speed)
        controller.set_spindle(int_speed / 60)
    if args.speed is None:
        try:
            controller.start()
        except KeyboardInterrupt:
            print("CTRL+C detected, exiting")
