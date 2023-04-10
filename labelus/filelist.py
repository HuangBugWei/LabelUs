from PyQt5.QtWidgets import QListWidget

class FileList(QListWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setMinimumWidth(140)
        self.setMaximumWidth(240)