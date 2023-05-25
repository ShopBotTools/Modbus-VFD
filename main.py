import argparse
from controller import VFDController

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=int,  help = "Port must be supplied with -p. Change the spindle speed, 7200-18000 currently")
parser.add_argument("-f", "--frequency", type=int,  help = "Port must be supplied with -p. Change the frequency, 120-300 currently")
parser.add_argument("-p", "--port", type=int, help = "Dictates the com port, enter 3 for COM3, 4 for COM4, etc...")
args = parser.parse_args()

if __name__ == "__main__":
    try:
        if args.port and args.speed:
            port_string = str(args.port)
            controller = VFDController(port_string)
            controller.connect(f"COM{port_string}")
            # Convert speed to frequency to pass to set_spindle
            int_speed = int(args.speed)
            controller.set_spindle(int_speed / 60)
        elif args.port and args.frequency:
            port_string = str(args.port)
            controller = VFDController(port_string)
            controller.connect(f"COM{port_string}")
            int_frequency = int(args.frequency)
            controller.set_frequency(int_frequency)
        else:
            controller = VFDController(3)
            controller.start()
    except KeyboardInterrupt:
        print("CTRL+C detected, exiting")
