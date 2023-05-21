import tkinter as tk
from tkinter import font
import minimalmodbus
import Modbus_Settings as MB
import threading

# Create a lock for synchronization
lock = threading.Lock()

def read_VFD(label_vars):
    # Create reading "instrument" called "reader" and import its settings from the Modbus settings module
    reader = minimalmodbus.Instrument(MB.USB_port, MB.mb_address)
    reader.mode = minimalmodbus.MODE_RTU
    reader.serial.parity = minimalmodbus.serial.PARITY_NONE
    reader.serial.baudrate = MB.baudrate
    reader.serial.bytesize = MB.bytesize
    reader.serial.stopbits = MB.stopbits
    reader.serial.timeout = MB.timeout
    reader.clear_buffers_before_each_transaction = MB.clear_buffers_before_call
    reader.close_port_after_each_call = MB.clear_buffers_after_call
    reader.debug = MB.debug

    def update_gui():
        with lock:
            try:
                # Read data from the device
                data = reader.read_registers(MB.read_frequency, MB.read_length, MB.READ_REGISTER)
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
                pass

            finally:
                reader.serial.close()

        # Schedule the next update
        root.after(2000, update_gui)  # Adjust the delay as needed (2000 milliseconds = 2 seconds)

    ################################GUI##################################
    root = tk.Tk()  # Create a root widget

    FONT_SIZE = font.Font(size=15)
    WINDOW_BACKGROUND = "white"
    FONT_BACKGROUND = "white"
    X_PADDING = 10

    root.title("Spindle Control")
    root.config(background=WINDOW_BACKGROUND)
    root.minsize(100, 100)  # width, height
    root.maxsize(1000, 1000)
    root.geometry("700x150+50+50")  # width x height + x + y

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

# Call the read_VFD() function to update the GUI
read_VFD({})
