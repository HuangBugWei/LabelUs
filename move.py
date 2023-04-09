import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt

class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(200,100,800,800)
        self.setWindowTitle('Example')

        # Load the original image and create a QPixmap object
        originalPixmap = QPixmap("./sample2-label1.png")

        # Create a new QPixmap object for the masked image
        maskedPixmap = QPixmap(originalPixmap.size())
        maskedPixmap.fill(QColor("transparent"))

        # Draw a black ellipse on the masked pixmap
        painter = QPainter(originalPixmap)
        painter.setBrush(QColor('blue'))
        painter.drawEllipse(200, 200, 300, 200)
        painter.end()
        self.xx = 0
        self.yy = 0
        # Create a new QLabel and set the masked pixmap as its pixmap
        self.label = QLabel(self)
        self.label.setPixmap(originalPixmap)
        self.label.move(self.xx, self.yy)
        # self.label.resize(maskedPixmap.width(), maskedPixmap.height())
        self.scale = 2
        self.label.resize(240*self.scale,180*self.scale)
        self.label.setScaledContents(True)

        self.show()
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Record the initial mouse position
            self.x, self.y = event.x(), event.y()
            self.xx, self.yy = self.label.x(), self.label.y()
            print(self.xx, self.yy)

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            # Calculate the difference between the initial position and the current position
            diff_x = event.x() - self.x
            diff_y = event.y() - self.y
            # self.xx += diff_x
            # self.yy += diff_y
            self.label.move(self.xx + diff_x, self.yy + diff_y)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
