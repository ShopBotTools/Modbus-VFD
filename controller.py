import minimalmodbus
from model import VFDModel
from view import VFDView
import modbus_settings as MB

class VFDController:
    def __init__(self, port):
        self.com_ports = ["COM1", "COM2", "COM3", "COM4"]
        self.selected_port = f"COM{port}"
        self.model = VFDModel(self.selected_port)
        self.view = VFDView(self, self.com_ports, self.selected_port)
        self.connected = False

    def connect(self, com_port):
        try:
            self.model = VFDModel(com_port)
            self.connected = True
            self.view.update_connection_status("Connected")
        except Exception as e:
            self.connected = False
            self.view.update_connection_status("Disconnected")
            self.view.show_error_message(f"Failed to connect to {com_port}: {str(e)}")

    def reconnect(self):
        selected_port = self.view.selected_com_port.get()
        self.model = VFDModel(selected_port)  # Reinitialize the model
        self.connect(selected_port)

    def read_vfd(self):
        if self.connected:
            try:
                frequency_data = self.model.read_VFD(MB.READ_FREQUENCY, MB.READ_LENGTH)
                self.view.update_labels(frequency_data)
            except minimalmodbus.ModbusException as e:
                # Handle modbus communication error
                print("Modbus Exception:", e)
            except Exception as e:
                # Handle other exceptions
                print("Exception:", e)
        else:
            self.reconnect()
        self.view.root.after(2000, self.read_vfd)

    def set_current(self, value):
        if self.connected:
            outcome = self.model.write_VFD(value)
            if outcome is False:
                self.view.show_error_message("Please enter a value between 60 and 120")
        else:
            self.reconnect()

    def start(self):
        self.view.start()
