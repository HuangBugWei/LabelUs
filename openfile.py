import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap

class button1(QPushButton):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.text = "lllllllllll"

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 400, 250)
        self.setWindowTitle('Example')

        self.btn = QPushButton('Select Image', self)
        
        self.btn.setGeometry(10, 10, 100, 30)
        self.btn.clicked.connect(self.openFileDialog)
        self.b = button1()
        self.label = QLabel(self)
        self.label.setGeometry(120, 10, 250, 230)
        self.label.setFrameStyle(QLabel.Box | QLabel.Sunken)

        self.show()

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.xpm *.jpg *.bmp *.gif)", options=options)
        if fileName:
            pixmap = QPixmap(fileName)
            self.label.setPixmap(pixmap)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
