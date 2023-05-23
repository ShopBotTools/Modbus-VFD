import tkinter as tk
from tkinter import font

class VFDView:
    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()

        self.label_vars = {
            "current": tk.StringVar(),
            "hirz": tk.StringVar(),
            "volt": tk.StringVar(),
            "bus": tk.StringVar(),
            "power": tk.StringVar(),
            "process": tk.StringVar()
        }

        self.FONT_SIZE = font.Font(size=15)
        self.WINDOW_BACKGROUND = "white"
        self.FONT_BACKGROUND = "white"
        self.X_PADDING = 10

    def create_gui(self):
        self.root.title("Spindle Control")
        self.root.config(background=self.WINDOW_BACKGROUND)
        self.root.minsize(100, 100)  # width, height
        self.root.maxsize(1000, 1000)
        self.root.geometry("700x200+50+50")  # width x height + x + y

        # Column 1, Keys
        self.current_label = tk.Label(self.root, text="Current", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.current_label.grid(row=1, column=1, padx=self.X_PADDING)

        self.frequency_label = tk.Label(self.root, text="Frequency", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.frequency_label.grid(row=2, column=1, padx=self.X_PADDING)

        self.output_voltage_label = tk.Label(self.root, text="Output Voltage", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.output_voltage_label.grid(row=3, column=1, padx=self.X_PADDING)

        self.dc_voltage_label = tk.Label(self.root, text="DC Bus Voltage", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.dc_voltage_label.grid(row=4, column=1, padx=self.X_PADDING)

        self.total_power_label = tk.Label(self.root, text="Total Power", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.total_power_label.grid(row=5, column=1, padx=self.X_PADDING)

        self.operation_code_label = tk.Label(self.root, text="Operation Code", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.operation_code_label.grid(row=6, column=1, padx=self.X_PADDING)

        # Column 2, Values
        self.current_value = tk.Label(self.root, textvariable=self.label_vars["current"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.current_value.grid(row=1, column=2, padx=self.X_PADDING)

        self.frequency_value = tk.Label(self.root, textvariable=self.label_vars["hirz"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.frequency_value.grid(row=2, column=2, padx=self.X_PADDING)

        self.output_voltage_value = tk.Label(self.root, textvariable=self.label_vars["volt"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.output_voltage_value.grid(row=3, column=2, padx=self.X_PADDING)

        self.dc_voltage_value = tk.Label(self.root, textvariable=self.label_vars["bus"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.dc_voltage_value.grid(row=4, column=2, padx=self.X_PADDING)

        self.total_power_value = tk.Label(self.root, textvariable=self.label_vars["power"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.total_power_value.grid(row=5, column=2, padx=self.X_PADDING)

        self.operation_code_value = tk.Label(self.root, textvariable=self.label_vars["process"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.operation_code_value.grid(row=6, column=2, padx=self.X_PADDING)

        # Create an entry widget for manual input of current value
        self.current_entry = tk.Entry(self.root, bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.current_entry.grid(row=1, column=3, padx=self.X_PADDING)

        # Button to set the current value
        self.set_current_button = tk.Button(self.root, text="Set Current", command=self.set_current)
        self.set_current_button.grid(row=1, column=4, padx=self.X_PADDING)

        self.root.iconbitmap("rpm.ico")

    def set_current(self):
        value = self.current_entry.get()
        if value:
            self.controller.set_current(value)

    def update_labels(self, data):
        current = data[0]
        hirz = data[1]
        volt = data[2]
        bus = data[3]
        power = data[4]
        process = data[5]

        self.label_vars["current"].set(f"{current / 10}A")
        self.label_vars["hirz"].set(f"{float(hirz / 100)}Hz")
        self.label_vars["volt"].set(f"{volt}V")
        self.label_vars["bus"].set(f"{bus}V")
        self.label_vars["power"].set(f"{power / 10}kW")
        self.label_vars["process"].set(str(process))

    def start(self):
        self.create_gui()
        self.root.after(0, self.controller.read_vfd)
        self.root.mainloop()