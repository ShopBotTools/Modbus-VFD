from model import VFDModel
from view import VFDView

class VFDController:
    def __init__(self):
        self.com_ports = ["COM1", "COM2", "COM3", "COM4"]
        self.model = VFDModel(self.com_ports[0])
        self.view = VFDView(self, self.com_ports)
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
            data = self.model.read_VFD()
            self.view.update_labels(data)
        else:
            self.reconnect()
        self.view.root.after(2000, self.read_vfd)

    def set_current(self, value):
        if self.connected:
            self.model.write_VFD(value)
        else:
            self.reconnect()

    def start(self):
        self.view.start()
