import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QSpacerItem, QSizePolicy
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from move import Example as ee
from move import myImage

class MyLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText('This is a QLabel')
        self.setAlignment(Qt.AlignCenter)
class MyLeft(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        button1 = QPushButton('Button 1')
        button2 = QPushButton('Button 2')
        button3 = QPushButton('Button 3')
        button4 = QPushButton('Button 4')
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(button1)
        buttonLayout.addWidget(button2)
        buttonLayout.addWidget(button3)
        buttonLayout.addWidget(button4)
        self.setMaximumWidth(100)
        self.setLayout(buttonLayout)

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Create the QLabel instance
        label = MyLabel()
        left = MyLeft()
        img = myImage()
        # Create a QHBoxLayout and add the button layout and label
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(left)
        mainLayout.addWidget(img)
        mainLayout.addWidget(label)

        # Set the main layout of the window
        self.setLayout(mainLayout)

        self.setGeometry(300, 300, 800, 850)
        self.setWindowTitle('Example')
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
