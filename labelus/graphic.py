from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QPointF, QEvent
from utils import *
import cv2

# modified from https://stackoverflow.com/a/35514531
class PhotoViewer(QtWidgets.QGraphicsView):

    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self._labelObjects = []
        
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap:
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap(pixmap))
            self._cv2img = cv2.imread(pixmap)
            self._cv2mask = creatMask(self._cv2img)
            self._currentMask = np.zeros_like(self._cv2img)

        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())
        
        # clean _labelMask on it
        while self._labelObjects:
            it = self._labelObjects.pop()
            self._scene.removeItem(it)
            del it

        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            
            if self._photo.isUnderMouse():
                
                self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
                print(self.mapToScene(event.pos()).toPoint())
            floodFillInput = (self.mapToScene(event.pos()).toPoint().x(),
                              self.mapToScene(event.pos()).toPoint().y())

            self._currentMask = floodFill(self._currentMask, self._cv2mask, 
                               floodFillInput,
                               (255, 255, 255),
                               (0, 0, 0),
                               (0, 0, 0))
            self.draw(self.mapToScene(event.pos()).toPoint())
        else:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
        super(PhotoViewer, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        

    def draw(self, p):
        it = QtWidgets.QGraphicsEllipseItem(0, 0, 50, 50)
        it.setPen(QtGui.QPen(QtCore.Qt.red, 5, QtCore.Qt.SolidLine))
        self._scene.addItem(it)
        it.setPos(p)
        self._labelObjects.append(it)
    

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.viewer = PhotoViewer(self)
        
        # Arrange layout
        VBlayout = QtWidgets.QVBoxLayout(self)
        VBlayout.addWidget(self.viewer)
        # self.loadImage()

    def loadImage(self, filename: str):
        self.viewer.setPhoto(QtGui.QPixmap(filename))

    def pixInfo(self):
        self.viewer.toggleDragMode()



if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.setGeometry(500, 300, 800, 600)
    window.show()
    sys.exit(app.exec_())