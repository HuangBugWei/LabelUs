import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog

from move import myImage

class MyLabel(QLabel):
    def __init__(self):
        super().__init__()
        self.setText('This is a QLabel')
        self.setAlignment(Qt.AlignCenter)

class Tools(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.button1 = QPushButton('Open \nImage')
        button2 = QPushButton('Button 2')
        button3 = QPushButton('Button 3')
        button4 = QPushButton('Button 4')
        self.button1.setFlat(True)
        
        # Set the size of the buttons
        self.button1.setFixedSize(80, 80)
        button2.setFixedSize(80, 80)
        button3.setFixedSize(80, 80)
        button4.setFixedSize(80, 80)
        
        # buttonLayout = QVBoxLayout()
        self.addWidget(self.button1)
        self.addWidget(button2)
        self.addWidget(button3)
        self.addWidget(button4)
        self.addStretch()
        self.setSpacing(0)
        
        # self.setAlignment(Qt.AlignmentFlag.AlignHCenter)
    

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Create the QLabel instance
        label = MyLabel()
        tools = Tools()
        tools.button1.clicked.connect(self.openFileDialog)
        self.img = myImage("")
        # Create a QHBoxLayout and add the button layout and label
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(tools)
        mainLayout.addWidget(self.img)
        mainLayout.addWidget(label)

        # Set the main layout of the window
        self.setLayout(mainLayout)

        self.setGeometry(300, 300, 800, 850)
        self.setMinimumSize(800, 800)
        self.setWindowTitle('Labelus')
        self.setContentsMargins(0,0,0,0)
        self.show()
    
    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if fileName:
            print(fileName)
            self.img.path = fileName
            self.img.update()
            # pixmap = QPixmap(fileName)
            # self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
