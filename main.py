from controller import VFDController
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=int,  help = "Change the spindle speed, 60-120 currently")
args = parser.parse_args()

if __name__ == "__main__":
    controller = VFDController()
    if args.speed:
        controller.set_current(args.speed)
    else:
        controller.start()