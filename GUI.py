import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QDialog, QGraphicsWidget
from PyQt5.QtGui import QPixmap

class MyClass(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("labelus")
        self.setGeometry(200,100,800,800)
        self.x = 0
        self.y = 0
        # self.showMaximized()
        self.lbl = QLabel(self)
        self.lbl.move(self.x, self.y)
        self.lbl.setPixmap(QPixmap("./sample2-label1.png"))
        self.scale = 2
        self.lbl.resize(240*self.scale,180*self.scale)
        self.lbl.setScaledContents(True)
        btn1 = QPushButton("down", self)
        btn1.clicked.connect(self.scaledown)
        btn2 = QPushButton("up", self)
        btn2.clicked.connect(self.scaleup)
        btn3 = QPushButton("left", self)
        btn3.clicked.connect(self.left)
        self.show()
    
    def scaledown(self):
        self.scale -= 1
        self.lbl.resize(240*self.scale,180*self.scale)
    def scaleup(self):
        self.scale += 1
        print(self.scale)
        self.lbl.resize(240*self.scale,180*self.scale)
    
    def left(self):
        self.x -= 50
        self.lbl.move(self.x, self.y)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mc = MyClass()
    app.exec_()
