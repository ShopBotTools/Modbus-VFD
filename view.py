import tkinter as tk
from tkinter import ttk
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
            "spindle_speed": tk.StringVar(),
            "load": tk.StringVar(),
            "connection": tk.StringVar()
        }

        self.FONT_SIZE = font.Font(size=14)
        self.WINDOW_BACKGROUND = "white"
        self.FONT_BACKGROUND = "white"
        self.X_PADDING = 10

        self.spindle_label        = None
        self.actual_speed_label   = None
        self.load_label           = None
        self.spindle_value        = None
        self.actual_speed_value   = None
        self.load_value           = None
        self.load_progress        = None
        self.spindle_entry        = None
        self.set_spindle_button   = None
        self.com_port_label       = None
        self.com_port_dropdown    = None
        self.connect_button       = None

    def create_gui(self):
        self.root.title("Spindle Control")
        self.root.config(background=self.WINDOW_BACKGROUND)
        self.root.minsize(100, 100)  # width, height
        self.root.maxsize(1000, 1000)
        self.root.geometry("750x175+165+735")  # width x height + x + y

        # Column 1, Keys
        self.spindle_label = tk.Label(self.root, text="Spindle Speed", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.spindle_label.grid(row=1, column=0, padx=self.X_PADDING)

        self.load_label = tk.Label(self.root, text="Spindle Load", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.load_label.grid(row=2, column=0, padx=self.X_PADDING)

        # Column 2, Values
        self.spindle_value = tk.Label(self.root, textvariable=self.label_vars["spindle_speed"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.spindle_value.grid(row=1, column=1, padx=self.X_PADDING)

        self.load_value = tk.Label(self.root, textvariable=self.label_vars["load"], bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.load_value.grid(row=2, column=1, padx=self.X_PADDING)

        self.load_progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=250)
        self.load_progress.grid(row=2, column=2, padx=self.X_PADDING, pady=10)

        # Create an entry widget for manual input of spindle speed value
        self.spindle_entry = tk.Entry(self.root, bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.spindle_entry.grid(row=1, column=2, padx=self.X_PADDING)
        self.spindle_entry.bind('<Return>', self.set_spindle)

        # Button to set the spindle speed value
        self.set_spindle_button = tk.Button(self.root, text="Set Spindle Speed", command=self.set_spindle)
        self.set_spindle_button.config(font=self.FONT_SIZE)
        self.set_spindle_button.grid(row=1, column=3, padx=self.X_PADDING, sticky="w")  # Set sticky parameter to "w" for left alignment)

        # COM Port selection dropdown menu
        self.com_port_label = tk.Label(self.root, text="COM Port", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.com_port_label.grid(row=3, column=0, padx=self.X_PADDING)
        self.com_port_dropdown = tk.OptionMenu(self.root, self.selected_com_port, *self.com_ports)
        self.com_port_dropdown.config(font=self.FONT_SIZE)
        self.com_port_dropdown.grid(row=3, column=1, padx=self.X_PADDING, sticky="e")  # Set sticky parameter to "e" for right alignment

        # Connect button
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.config(font=self.FONT_SIZE)
        self.connect_button.grid(row=3, column=2, padx=self.X_PADDING, sticky="w")  # Set sticky parameter to "w" for left alignment

        if not self.controller.model.connected:
            self.spindle_entry.configure(state="disabled")
            self.set_spindle_button.configure(state="disabled")
            for var in self.label_vars.values():
                var.set("Disconnected")

        self.root.iconbitmap(bitmap="")

    def update_connection_status(self, status):
        self.label_vars["connection"].set(status)

    def show_error_message(self, message):
        messagebox.showerror("Error", message)

    # Optional event parameter is for using enter key
    def set_spindle(self, event = None):
        value = self.spindle_entry.get()
        if value:
            int_value = int(value)
            self.controller.set_spindle(int_value / 60)
            self.spindle_entry.delete(0, 'end')

    def update_labels(self, data):
        spindle = data[0]
        load = data[2]

        spindle_value = round((spindle/ 10) * 60, 1)

        # Divide the decimal response by the highest possible value of 1 byte (255)
        # Then multiply that number by 100 to produce a percentage
        load_percentage = round((load / 255) * 100)

        self.label_vars["spindle_speed"].set(f"{spindle_value} RPM")
        self.label_vars["load"].set(f"{load_percentage}%")
        self.load_progress["value"] = load_percentage

    def start(self):
        self.create_gui()
        self.root.after(0, self.controller.read_vfd)
        self.root.mainloop()

    def connect(self):
        selected_port = self.selected_com_port.get()
        self.controller.connect(selected_port)
        self.spindle_entry.configure(state="normal")
        self.set_spindle_button.configure(state="normal")
        for var in self.label_vars.values():
            var.set("")

        if not self.controller.model.connected:
            self.spindle_entry.configure(state="disabled")
            self.set_spindle_button.configure(state="disabled")
            for var in self.label_vars.values():
                var.set("Disconnected")
        else:
            self.controller.read_vfd()
