from PyQt5.QtWidgets import QVBoxLayout, QPushButton

class Tools(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button1 = QPushButton('Open \nImage')
        self.button2 = QPushButton('Open \nFolder')
        self.button3 = QPushButton('Save')
        self.button4 = QPushButton('Undo')
        
        # Set the size of the buttons
        self.button1.setFixedSize(80, 80)
        self.button2.setFixedSize(80, 80)
        self.button3.setFixedSize(80, 80)
        self.button4.setFixedSize(80, 80)
        
        # buttonLayout = QVBoxLayout()
        self.addWidget(self.button1)
        self.addWidget(self.button2)
        self.addWidget(self.button3)
        self.addWidget(self.button4)
        self.addStretch()
        self.setSpacing(0)
        
        # self.setAlignment(Qt.AlignmentFlag.AlignHCenter)