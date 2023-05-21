import tkinter as tk
from tkinter import font
import minimalmodbus
import threading
import argparse
import user_inputs

########################### Modbus settings ###########################
## Set the Modbus paramaters in here for both reading and writing to the VFD
## General Modbus Settings

MB_ADDRESS = 3                          # Station Address
USB_PORT = "COM3"                       # Location of USB to RS485 converter
BAUDRATE = 9600                         # BAUDRATE
BYTESIZE = 8                            # Number of data bits to be requested
STOPBITS = 1                            # Number of stop bits
TIMEOUT = 0.5                           # TIMEOUT time in seconds
CLEAR_BUFFERS_BEFORE_CALL = True        # Good practice clean up
CLEAR_BUFFERS_AFTER_CALL  = True        # Good practice clean up
DEBUG = True

## P194
PASSWORD = 0

## Registers
READ_FREQUENCY    = 24
SET_FREQUENCY     = 44
UNLOCK_DRIVE      = 48
UNLOCK_PARAMETERS = 49

# Define Modbus function codes
READ_REGISTER         = 3
WRITE_SINGLE_REGISTER = 6

## Read Settings
READ_LENGTH = 6                # Number of adresses to read when Polling the VFD for data
#////////////////////////// Modbus Settings //////////////////////////#



########################### Command Line Arguments ###########################
parser = argparse.ArgumentParser()
parser.add_argument("-s", "--speed", type=int,  help = "Change the spindle speed, 60-120 currently")
args = parser.parse_args()
#////////////////////////// Command Line Arguments //////////////////////////#



# Create a lock for reading and writing synchronization
lock = threading.Lock()

############################### Writing the VFD ##############################
def write_VFD():
    ## Create writing "instrument" that can perform write operations and import it's settings from the modbus settings module
    writer = minimalmodbus.Instrument(USB_PORT, MB_ADDRESS)
    writer.mode = minimalmodbus.MODE_RTU
    writer.serial.parity = minimalmodbus.serial.PARITY_NONE
    writer.serial.baudrate = BAUDRATE
    writer.serial.bytesize = BYTESIZE
    writer.serial.stopbits = STOPBITS
    writer.serial.timeout  = TIMEOUT
    writer.clear_buffers_before_each_transaction = CLEAR_BUFFERS_BEFORE_CALL
    writer.close_port_after_each_call = CLEAR_BUFFERS_AFTER_CALL
    writer.debug = DEBUG

    speed_set = False
    speed_package = user_inputs.set_user_speed(args.speed)
    if speed_package != "NaN" and speed_package != "OL":
        speed_set = True
    
    ## Send the request to the vfd
    def send_to_vfd(register, data, function_code, decimals = 0, signed = False):
        with lock:
            writer.write_register(register, data, decimals, function_code, signed)
            writer.serial.close()

    # If the speed has been set correctly then pass on the speed package as
    # well as the register position to the function to send to the VFD
    if speed_set:
        print("Attempting unlock drive")
        send_to_vfd(UNLOCK_DRIVE, PASSWORD, WRITE_SINGLE_REGISTER)
        print("Attempting unlock parameters")
        send_to_vfd(UNLOCK_PARAMETERS, PASSWORD, WRITE_SINGLE_REGISTER)
        print("Attempting set frequency")
        send_to_vfd(SET_FREQUENCY, speed_package, WRITE_SINGLE_REGISTER)
#////////////////////////////// Writing the VFD /////////////////////////////#


############################### Reading the VFD ##############################
def read_VFD(label_vars):
    # Create reading "instrument" called "reader" and import its settings from the Modbus settings module
    reader = minimalmodbus.Instrument(USB_PORT, MB_ADDRESS)
    reader.mode = minimalmodbus.MODE_RTU
    reader.serial.parity = minimalmodbus.serial.PARITY_NONE
    reader.serial.baudrate = BAUDRATE
    reader.serial.bytesize = BYTESIZE
    reader.serial.STOPBITS = STOPBITS
    reader.serial.timeout = TIMEOUT
    reader.clear_buffers_before_each_transaction = CLEAR_BUFFERS_BEFORE_CALL
    reader.close_port_after_each_call = CLEAR_BUFFERS_AFTER_CALL
    reader.debug = DEBUG

    def update_gui():
        with lock:
            try:
                # Read data from the device
                data = reader.read_registers(READ_FREQUENCY, READ_LENGTH, READ_REGISTER)
                reader.serial.close()

                # Split out the list into individual variables
                current = data[0]
                hirz = data[1]
                volt = data[2]
                bus = data[3]
                power = data[4]
                process = data[5]

                # Update the label variables with the new values
                label_vars["current"].set(f"{current / 10}A")
                label_vars["hirz"].set(f"{float(hirz / 100)}Hz")
                label_vars["volt"].set(f"{volt}V")
                label_vars["bus"].set(f"{bus}V")
                label_vars["power"].set(f"{power / 10}kW")
                label_vars["process"].set(str(process))

            except minimalmodbus.ModbusException:
                # Handle modbus communication error
                print("Something went wrong while reading")
                pass

            finally:
                reader.serial.close()

        # Schedule the next update
        root.after(2000, update_gui)  # Adjust the delay as needed (2000 milliseconds = 2 seconds)
#//////////////////////////// Reading the VFD ///////////////////////////////#



################################### GUI ######################################
    root = tk.Tk()  # Create a root widget

    FONT_SIZE = font.Font(size=15)
    WINDOW_BACKGROUND = "white"
    FONT_BACKGROUND = "white"
    X_PADDING = 10

    root.title("Spindle Control")
    root.config(background=WINDOW_BACKGROUND)
    root.minsize(100, 100)  # width, height
    root.maxsize(1000, 1000)
    root.geometry("700x200+50+50")  # width x height + x + y

    # Create label variables using StringVar
    label_vars = {
        "current": tk.StringVar(),
        "hirz": tk.StringVar(),
        "volt": tk.StringVar(),
        "bus": tk.StringVar(),
        "power": tk.StringVar(),
        "process": tk.StringVar()
    }

    # Column 1, Keys
    current_label = tk.Label(root, text="Current", bg=FONT_BACKGROUND, font=FONT_SIZE)
    current_label.grid(row=1, column=1, padx=X_PADDING)

    frequency_label = tk.Label(root, text="Frequency", bg=FONT_BACKGROUND, font=FONT_SIZE)
    frequency_label.grid(row=2, column=1, padx=X_PADDING)

    output_voltage_label = tk.Label(root, text="Output Voltage", bg=FONT_BACKGROUND, font=FONT_SIZE)
    output_voltage_label.grid(row=3, column=1, padx=X_PADDING)

    dc_voltage_label = tk.Label(root, text="DC Bus Voltage", bg=FONT_BACKGROUND, font=FONT_SIZE)
    dc_voltage_label.grid(row=4, column=1, padx=X_PADDING)

    total_power_label = tk.Label(root, text="Total Power", bg=FONT_BACKGROUND, font=FONT_SIZE)
    total_power_label.grid(row=5, column=1, padx=X_PADDING)

    operation_code_label = tk.Label(root, text="Operation Code", bg=FONT_BACKGROUND, font=FONT_SIZE)
    operation_code_label.grid(row=6, column=1, padx=X_PADDING)

    # Column 2, Values
    current_value = tk.Label(root, textvariable=label_vars["current"], bg=FONT_BACKGROUND, font=FONT_SIZE)
    current_value.grid(row=1, column=2, padx=X_PADDING)

    frequency_value = tk.Label(root, textvariable=label_vars["hirz"], bg=FONT_BACKGROUND, font=FONT_SIZE)
    frequency_value.grid(row=2, column=2, padx=X_PADDING)

    output_voltage_value = tk.Label(root, textvariable=label_vars["volt"], bg=FONT_BACKGROUND, font=FONT_SIZE)
    output_voltage_value.grid(row=3, column=2, padx=X_PADDING)

    dc_voltage_value = tk.Label(root, textvariable=label_vars["bus"], bg=FONT_BACKGROUND, font=FONT_SIZE)
    dc_voltage_value.grid(row=4, column=2, padx=X_PADDING)

    total_power_value = tk.Label(root, textvariable=label_vars["power"], bg=FONT_BACKGROUND, font=FONT_SIZE)
    total_power_value.grid(row=5, column=2, padx=X_PADDING)

    operation_code_value = tk.Label(root, textvariable=label_vars["process"], bg=FONT_BACKGROUND, font=FONT_SIZE)
    operation_code_value.grid(row=6, column=2, padx=X_PADDING)

    # Stop button
    def stop_update():
        root.after_cancel(update_id)

    root.iconbitmap("rpm.ico")

    # Start the initial update
    update_id = root.after(0, update_gui)
    root.mainloop()
#////////////////////////////////// GUI //////////////////////////////////#


# If a command line argument was specified, do that, otherwise read the VFD
if args.speed:
    write_VFD()
else:
    read_VFD({})
