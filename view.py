import tkinter as tk
from tkinter import font
from tkinter import messagebox

class VFDView:
    def __init__(self, controller, com_ports, port):
        self.root = tk.Tk()
        self.com_ports = com_ports
        self.selected_com_port = tk.StringVar()
        self.selected_com_port.set(port)  # Set the default selected COM port
        self.controller = controller

        self.label_vars = {
            "current": tk.StringVar(),
            "hirz": tk.StringVar(),
            "volt": tk.StringVar(),
            "bus": tk.StringVar(),
            "power": tk.StringVar(),
            "connection": tk.StringVar()
        }

        self.FONT_SIZE = font.Font(size=15)
        self.WINDOW_BACKGROUND = "white"
        self.FONT_BACKGROUND = "white"
        self.X_PADDING = 10

        # Initialize labels
        self.com_port_label = None
        self.com_port_dropdown = None
        self.connect_button = None
        self.current_label = None
        self.frequency_label = None
        self.output_voltage_label = None
        self.dc_voltage_label = None
        self.total_power_label = None
        self.current_value = None
        self.frequency_value = None
        self.output_voltage_value = None
        self.dc_voltage_value = None
        self.total_power_value = None
        self.current_entry = None
        self.set_current_button = None
        self.com_port_dropdown = None
        self.com_port_dropdown = None
        self.com_port_dropdown = None
        self.com_port_dropdown = None
        self.com_port_dropdown = None
        self.com_port_dropdown = None

    def create_gui(self):
        self.root.title("Spindle Control")
        self.root.config(background=self.WINDOW_BACKGROUND)
        self.root.minsize(100, 100)  # width, height
        self.root.maxsize(1000, 1000)
        self.root.geometry("750x200+50+50")  # width x height + x + y

        # COM Port selection dropdown menu
        self.com_port_label = tk.Label(self.root, text="COM Port", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.com_port_label.grid(row=0, column=0, padx=self.X_PADDING)

        self.com_port_dropdown = tk.OptionMenu(self.root, self.selected_com_port, *self.com_ports)
        self.com_port_dropdown.config(font=self.FONT_SIZE)
        self.com_port_dropdown.grid(row=0, column=1, padx=self.X_PADDING)

        # Connect button
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=2, padx=self.X_PADDING)

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

        # Create an entry widget for manual input of current value
        self.current_entry = tk.Entry(self.root, bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.current_entry.grid(row=1, column=3, padx=self.X_PADDING)

        # Button to set the current value
        self.set_current_button = tk.Button(self.root, text="Set Current", command=self.set_current)
        self.set_current_button.grid(row=1, column=4, padx=self.X_PADDING)
        self.root.bind('<Return>', self.set_current)

        if self.controller.model.disconnected:
            self.current_entry.configure(state="disabled")
            self.set_current_button.configure(state="disabled")
            for var in self.label_vars.values():
                var.set("Disconnected")

        self.root.iconbitmap("rpm.ico")

    def update_connection_status(self, status):
        self.label_vars["connection"].set(status)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    # Optional event parameter is for using enter key
    def set_current(self, event = None):
        value = self.current_entry.get()
        if value:
            self.controller.set_current(value)
            self.current_entry.delete(0, 'end')

    def update_labels(self, data):
        current = data[0]
        hirz = data[1]
        volt = data[2]
        bus = data[3]
        power = data[4]

        self.label_vars["current"].set(f"{current / 10}A")
        self.label_vars["hirz"].set(f"{float(hirz / 100)}Hz")
        self.label_vars["volt"].set(f"{volt}V")
        self.label_vars["bus"].set(f"{bus}V")
        self.label_vars["power"].set(f"{power / 10}kW")

    def start(self):
        self.create_gui()
        self.root.after(0, self.controller.read_vfd())
        self.root.mainloop()

    def connect(self):
        selected_port = self.selected_com_port.get()
        self.controller.connect(selected_port)
        self.current_entry.configure(state="normal")
        self.set_current_button.configure(state="normal")
        for var in self.label_vars.values():
            var.set("")

        if self.controller.model.disconnected:
            self.current_entry.configure(state="disabled")
            self.set_current_button.configure(state="disabled")
            for var in self.label_vars.values():
                var.set("Disconnected")
        else:
            self.controller.read_vfd()
