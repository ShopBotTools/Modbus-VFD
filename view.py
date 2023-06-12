import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import tempfile
import base64
import zlib
import re

# Create transparent icon to replace the default
ICON = zlib.decompress(base64.b64decode('eJxjYGAEQgEBBiDJwZDBy'
    'sAgxsDAoAHEQCEGBQaIOAg4sDIgACMUj4JRMApGwQgF/ykEAFXxQRc='))

_, ICON_PATH = tempfile.mkstemp()
with open(ICON_PATH, 'wb') as icon_file:
    icon_file.write(ICON)

# Custom validation function to limit the entry to 5 characters
def validate_entry(new_value):
    # Check if the new value matches the desired pattern (up to 5 characters)
    if re.match(r'^\d{0,5}$', new_value):
        return True
    else:
        messagebox.showwarning("Invalid Entry", "Please enter up to 5 numeric characters.")
        return False

class VFDView:
    def __init__(self, controller, com_ports, port):
        self.root = tk.Tk()
        self.com_ports = com_ports
        self.selected_com_port = tk.StringVar()
        self.selected_adjustment_options = [10, 100, 1000]
        self.selected_adjustment = tk.StringVar()
        self.selected_com_port.set(port)  # Set the default selected COM port
        self.selected_adjustment.set(self.selected_adjustment_options[2])
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
        self.Y_PADDING = 10
        self.LOAD_BAR_SIZE = 250

        self.spindle_label        = None
        self.load_label           = None
        self.spindle_value        = None
        self.load_value           = None
        self.load_progress        = None
        self.spindle_entry        = None
        self.set_spindle_button   = None
        self.com_port_label       = None
        self.com_port_dropdown    = None
        self.connect_button       = None
        self.increment_button     = None
        self.decrement_button     = None
        self.adjustment_dropdown  = None
        self.override_label       = None

    def position_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width) - (width)
        y = (screen_height // 2) - (height // 2)
        return x, y

    def create_gui(self):
        self.root.title("Spindle Control")
        self.root.config(background=self.WINDOW_BACKGROUND)
        self.root.minsize(100, 100)
        self.root.maxsize(1000, 1000)

        # Set the desired width and height for your app
        width = 900
        height = 100

        # Center the window based on screen size
        x, y = self.position_window(width, height)

        # Adjust the window position
        x -= 25
        y += 250

        self.root.geometry(f"{width}x{height}+{x}+{y}")

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

        self.load_progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=self.LOAD_BAR_SIZE)
        self.load_progress.grid(row=2, column=2, padx=self.X_PADDING, pady=self.Y_PADDING)

        # Create an entry widget for manual input of spindle speed value
        self.spindle_entry = tk.Entry(self.root, bg=self.FONT_BACKGROUND, font=self.FONT_SIZE, width=6, validate="key")
        self.spindle_entry.config(validatecommand=(self.spindle_entry.register(validate_entry), '%P'))
        self.spindle_entry.grid(row=1, column=2, padx=self.X_PADDING, sticky="w")

        def on_return(event):
            self.set_spindle()
        self.spindle_entry.bind('<Return>', on_return)

        def on_focus_out(event):
            self.root.focus_set()
        self.spindle_entry.bind('<FocusOut>', on_focus_out)

        # Button to set the spindle speed value
        self.set_spindle_button = tk.Button(self.root, text="Set Spindle Speed", command=self.set_spindle)
        self.set_spindle_button.config(font=self.FONT_SIZE)
        self.set_spindle_button.grid(row=1, column=2, padx=self.X_PADDING, sticky="e")  # Set sticky parameter to "w" for left alignment)

        # COM Port selection dropdown menu
        self.com_port_label = tk.Label(self.root, text="COM Port", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.com_port_label.grid(row=2, column=3, padx=self.X_PADDING, sticky="e")
        self.com_port_dropdown = tk.OptionMenu(self.root, self.selected_com_port, *self.com_ports)
        self.com_port_dropdown.config(font=10)
        self.com_port_dropdown.grid(row=2, column=4, padx=self.X_PADDING, pady=self.Y_PADDING, sticky="e")

        # Connect button
        self.connect_button = tk.Button(self.root, text="Connect", command=self.connect)
        self.connect_button.config(font=self.FONT_SIZE)
        self.connect_button.grid(row=2, column=5, padx=self.X_PADDING, sticky="w")

        # Decrement, - button
        self.decrement_button = tk.Button(self.root, text="  -  ", command=self.decrement_spindle)
        self.decrement_button.config(font=self.FONT_SIZE)
        self.decrement_button.grid(row=1, column=5, padx=0, sticky="w")
        self.root.bind('-', self.decrement_spindle)

        # Increment dropdown menu
        self.adjustment_dropdown = tk.OptionMenu(self.root, self.selected_adjustment, *self.selected_adjustment_options)
        self.adjustment_dropdown.config(font=self.FONT_SIZE)
        self.adjustment_dropdown.grid(row=1, column=4, padx=5, sticky="e")

        # Increment, + button
        self.increment_button = tk.Button(self.root, text="  +  ", command=self.increment_spindle)
        self.increment_button.config(font=self.FONT_SIZE)
        self.increment_button.grid(row=1, column=5, padx=50)
        self.root.bind('=', self.increment_spindle)

        # Override label
        self.override_label = tk.Label(self.root, text="Override", bg=self.FONT_BACKGROUND, font=self.FONT_SIZE)
        self.override_label.grid(row=1, column=3, padx=self.X_PADDING, sticky="e")

        if not self.controller.model.connected:
            self.spindle_entry.configure(state="disabled")
            self.set_spindle_button.configure(state="disabled")
            for var in self.label_vars.values():
                var.set("Disconnected")

        self.root.iconbitmap(default=ICON_PATH)

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

    def increment_spindle(self, event = None):
        value = self.label_vars["spindle_speed"].get()
        if value:
            int_value = int(value)
            incremented_value = int_value + int(self.selected_adjustment.get())
            incremented_value = min(incremented_value, 18000)
            print(incremented_value)
            self.controller.adjust_spindle(incremented_value)

    def decrement_spindle(self, event = None):
        value = self.label_vars["spindle_speed"].get()
        if value:
            int_value = int(value)
            decremented_value = int_value - int(self.selected_adjustment.get())
            decremented_value = max(decremented_value, 7200)
            print(decremented_value)
            self.controller.adjust_spindle(decremented_value)

    def update_labels(self, data):
        spindle                = data[0]
        # frequency            = data[1]
        load                   = data[2]
        # operation_status     = data[3]
        # direction            = data[4]
        # control_mode         = data[5] # P100
        # speed_command_source = data[6]
        # auto_manual_status   = data[7]
        # present_fault        = data[8]
        # command_rotation     = data[9]

        spindle_value = round((spindle/ 10) * 60)
        spindle_value = int(spindle_value)

        # Divide the decimal response by the highest possible value of 1 byte (256)
        load_percentage = round(load / 256)

        self.label_vars["spindle_speed"].set(spindle_value)
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
