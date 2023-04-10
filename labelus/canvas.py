from PyQt5.QtWidgets import QLabel, QFrame
from PyQt5.QtGui import QPixmap, QCursor
from PyQt5.QtCore import Qt

class Canvas(QLabel):
    def __init__(self, path=None):
        super().__init__()
        self.path = path if path else ""
        self.originalPixmap = QPixmap(self.path)
        self.scale = 1
        self.x, self.y = self.width(), self.height()
        self.xx = 0
        self.yy = 0
        self.initUI()
    
    def initUI(self):
        self.autoFillBackground()
        self.setFrameShape(QFrame.StyledPanel)
        
        # self.originalPixmap = QPixmap("./sample2-label1.png")
        
        # painter
        '''
        maskedPixmap = QPixmap(self.originalPixmap.size())
        maskedPixmap.fill(QColor("transparent"))
        # Draw a black ellipse on the masked pixmap
        painter = QPainter(self.originalPixmap)
        painter.setBrush(QColor('blue'))
        painter.drawEllipse(200, 200, 300, 200)
        painter.end()
        '''
        # Create a new QLabel and set the masked pixmap as its pixmap
        self.label = QLabel(self)
        
        self.label.setPixmap(self.originalPixmap)
        # self.label.move(self.xx, self.yy)
        # self.label.resize(maskedPixmap.width(), maskedPixmap.height())

        self.label.resize(240*self.scale, 180*self.scale)
        self.label.setScaledContents(True)

        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.show()
    def update(self):
        self.label.setPixmap(QPixmap(self.path))

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            # Record the initial mouse position
            self.x, self.y = event.x(), event.y()
            self.xx, self.yy = self.label.x(), self.label.y()
            print(self.xx, self.yy)
        elif event.button() == Qt.LeftButton:
            globalPos = QCursor.pos()
            widgetPos = self.label.mapFromGlobal(globalPos)
            # Global position -> full screen position
            print('Global position:', globalPos.x(), globalPos.y())
            # Widget position -> parent widget position
            print('Widget position:', widgetPos.x(), widgetPos.y())

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.RightButton:
            # Calculate the difference between the initial position and the current position
            diff_x = event.x() - self.x
            diff_y = event.y() - self.y
            # self.xx += diff_x
            # self.yy += diff_y
            self.label.move(self.xx + diff_x, self.yy + diff_y)

    def wheelEvent(self, event):
        # Print the number of degrees the mouse wheel was rotated
        angle = event.angleDelta().y() / 8
        print('Wheel event:', event.angleDelta().y() / 8)
        if (angle > 0):
            self.scale += 0.5
        else:
            if self.scale > 1:
                self.scale -= 0.5
            else:
                self.scale -= 0.05
        ogw = self.label.width()
        ogh = self.label.height()
        globalPos = QCursor.pos()
        widgetPos = self.label.mapFromGlobal(globalPos)
        cursorx, cursory = widgetPos.x(), widgetPos.y()
        self.label.resize(240*self.scale,180*self.scale)
        neww = self.label.width()
        newh = self.label.height()
        
        
        self.xx -= cursorx * (neww /ogw - 1)
        self.yy -= cursory * (newh / ogh - 1)
        # self.yy = self.height() / 2 - self.label.height() / 2
        # self.xx = self.width() / 2 - self.label.width() / 2
        self.label.move(self.xx, self.yy)
        print(self.width())
        print(self.label.width())