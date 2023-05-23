from model import VFDModel
from view import VFDView

class VFDController:
    def __init__(self):
        self.model = VFDModel()
        self.view = VFDView(self)

    def read_vfd(self):
        data = self.model.read_VFD()
        self.view.update_labels(data)
        self.view.root.after(2000, self.read_vfd)

    def set_current(self, value):
        self.model.write_VFD(value)

    def start(self):
        self.view.start()