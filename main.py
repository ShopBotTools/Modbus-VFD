from controller import VFDController
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=int,  help = "Port must be supplied with -p. Change the spindle speed, 60-120 currently")
parser.add_argument("-p", "--port", type=int, help = "Dictates the com port, enter 3 for COM3, 4 for COM4, etc...")
args = parser.parse_args()

if __name__ == "__main__":
    if args.port and args.speed:
        port_string = str(args.port)
        print(f"Port: {port_string}")
        controller = VFDController(port_string)
        controller.connect(f"COM{port_string}")
        if args.speed:
            print(f"Speed: {args.speed}")
            controller.set_current(args.speed)
    else:
        controller = VFDController(3)
        controller.start()
