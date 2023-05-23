import tkinter as tk
from tkinter import font
import minimalmodbus
import threading
from time import sleep
import modbus_settings as MB
import user_inputs
import command_line_interface as cli

# Create a lock for reading and writing synchronization
lock = threading.Lock()

############################### Writing the VFD ##############################
def write_VFD(user_input):
    ## Create writing "instrument" that can perform write operations and import it's settings from the modbus settings module
    writer = minimalmodbus.Instrument(MB.USB_PORT, MB.MB_ADDRESS)
    writer.mode = minimalmodbus.MODE_RTU
    writer.serial.parity = minimalmodbus.serial.PARITY_NONE
    writer.serial.baudrate = MB.BAUDRATE
    writer.serial.bytesize = MB.BYTESIZE
    writer.serial.stopbits = MB.STOPBITS
    writer.serial.timeout  = MB.TIMEOUT
    writer.clear_buffers_before_each_transaction = MB.CLEAR_BUFFERS_BEFORE_CALL
    writer.close_port_after_each_call = MB.CLEAR_BUFFERS_AFTER_CALL
    writer.debug = MB.DEBUG

    speed_set = False
    speed_package = user_inputs.set_user_speed(user_input)

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
        send_to_vfd(MB.UNLOCK_DRIVE, MB.PASSWORD, MB.WRITE_SINGLE_REGISTER)
        print("Attempting unlock parameters")
        send_to_vfd(MB.UNLOCK_PARAMETERS, MB.PASSWORD, MB.WRITE_SINGLE_REGISTER)
        print("Attempting set frequency")
        send_to_vfd(MB.SET_FREQUENCY, speed_package, MB.WRITE_SINGLE_REGISTER)
#////////////////////////////// Writing the VFD /////////////////////////////#


############################### Reading the VFD ##############################
def read_VFD(label_vars):
    # Create reading "instrument" called "reader" and import its settings from the Modbus settings module
    reader = minimalmodbus.Instrument(MB.USB_PORT, MB.MB_ADDRESS)
    reader.mode = minimalmodbus.MODE_RTU
    reader.serial.parity = minimalmodbus.serial.PARITY_NONE
    reader.serial.baudrate = MB.BAUDRATE
    reader.serial.bytesize = MB.BYTESIZE
    reader.serial.stopbits = MB.STOPBITS
    reader.serial.timeout = MB.TIMEOUT
    reader.clear_buffers_before_each_transaction = MB.CLEAR_BUFFERS_BEFORE_CALL
    reader.close_port_after_each_call = MB.CLEAR_BUFFERS_AFTER_CALL
    reader.debug = MB.DEBUG

    def update_gui():
        with lock:
            try:
                # Read data from the device
                data = reader.read_registers(MB.READ_FREQUENCY, MB.READ_LENGTH, MB.READ_REGISTER)
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

            except minimalmodbus.ModbusException as e:
                # Handle modbus communication error
                print("Modbus Exception:", e)
                # Update GUI or show an error message to the user
                label_vars["process"].set("Error: Modbus Exception")
            except Exception as e:
                # Handle other exceptions
                print("Exception:", e)
                # Update GUI or show an error message to the user
                label_vars["process"].set("Error: Unknown Exception")

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

    # Create an entry widget for manual input of current value
    current_entry = tk.Entry(root, bg=FONT_BACKGROUND, font=FONT_SIZE)
    current_entry.grid(row=1, column=3, padx=X_PADDING)

    # Function to call when set current button is pressed
    def set_current():
        value = current_entry.get()
        if value:
            write_VFD(value)
    # Button to set the current value
    set_current_button = tk.Button(root, text="Set Current", command=set_current)
    set_current_button.grid(row=1, column=4, padx=X_PADDING)

    root.iconbitmap("rpm.ico")

    # Start the initial update
    root.after(0, update_gui)
    root.mainloop()
#////////////////////////////////// GUI //////////////////////////////////#


# If a command line argument was specified, do that, otherwise read the VFD
if cli.args.speed:
        write_VFD(cli.args.speed)
else:
    sleep(3)
    read_VFD({})
