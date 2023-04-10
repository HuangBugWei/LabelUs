import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog
from PyQt5.QtGui import QResizeEvent

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

        self.setGeometry(100, 100, 1080, 720)
        self.setMinimumSize(1080, 720)
        self.setWindowTitle('Labelus')
        self.setContentsMargins(0,0,0,0)
        self.show()

    def resizeEvent(self, event):
        print('Current size:', self.size().width(), 'x', self.size().height())
        self.img.yy = self.img.height() / 2 - self.img.label.height() / 2
        self.img.xx = self.img.width() / 2 - self.img.label.width() / 2
        self.img.update()
        print('canvas size:', self.img.width(), 'x', self.img.height())
        print('canvas size:', self.img.label.width(), 'x', self.img.label.height())
        super().resizeEvent(event)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if fileName:
            print(fileName)
            self.img.path = fileName
            print('oepn canvas size:', self.img.width(), 'x', self.img.height())
            
            self.img.update()
            # pixmap = QPixmap(fileName)
            # self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
