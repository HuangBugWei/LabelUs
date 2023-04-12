from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QPointF, QEvent
from utils import *
import cv2, os, json, base64
import numpy as np

# modified from https://stackoverflow.com/a/35514531
class PhotoViewer(QtWidgets.QGraphicsView):

    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent):
        super(PhotoViewer, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._tempMask = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self._scene.addItem(self._tempMask)
        self._labelObjects = []
        self._tempLabelObjects = []
        self._labelNow = False
        self._imgPath = None
        
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(0, 255, 0)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        shortcutUndo = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self)
        shortcutUndo.activated.connect(self.undo)

        shortcutStore = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        shortcutStore.activated.connect(self.store)

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
            self._imgPath = os.path.basename(pixmap)
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
        
        while self._tempLabelObjects:
            it = self._tempLabelObjects.pop()
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

    def undo(self):
        if self._tempLabelObjects:
            self._tempLabelObjects.pop()
            if self._tempLabelObjects:
                self._currentMask = self._tempLabelObjects.pop()
                self.drawTempMask(self._currentMask)
            else:
                self._tempMask.setPixmap(QtGui.QPixmap())
                self._currentMask[self._currentMask > 0] = 0
        elif self._labelObjects:
            it = self._labelObjects.pop()
            self._scene.removeItem(it[0])
            del it
        

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            print(self._cv2img.shape)
            self._labelNow = True
            floodFillInput = (self.mapToScene(event.pos()).toPoint().x(),
                              self.mapToScene(event.pos()).toPoint().y())

            self._currentMask, isSame = floodFill(self._currentMask, self._cv2mask, 
                                                    floodFillInput,
                                                    (255, 255, 255),
                                                    (0, 0, 0),
                                                    (0, 0, 0))
            
            if not isSame:
                self.drawTempMask(self._currentMask)
        else:
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            
        super(PhotoViewer, self).mousePressEvent(event)

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:
        # if event.button() == Qt.RightButton:
        if self._labelNow:
            if self._photo.isUnderMouse():
                self.photoClicked.emit(self.mapToScene(event.pos()).toPoint())
                
            floodFillInput = (self.mapToScene(event.pos()).toPoint().x(),
                              self.mapToScene(event.pos()).toPoint().y())

            self._currentMask, isSame = floodFill(self._currentMask, self._cv2mask, 
                                                    floodFillInput,
                                                    (255, 255, 255),
                                                    (0, 0, 0),
                                                    (0, 0, 0))
            
            if not isSame:
                self.drawTempMask(self._currentMask)
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        if event.button() == Qt.LeftButton:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif event.button() == Qt.RightButton:
            self._labelNow = False
        super(PhotoViewer, self).mouseReleaseEvent(event)
        

    def drawTempMask(self, mask):
        arr = np.transpose(dilate(mask), (2, 0, 1))[0] > 0
        new_arr = np.zeros(arr.shape + (4,), dtype=np.uint8)
        # new_arr[arr] = np.array(QColor('red').getRgb()[:3] + (255,))
        new_arr[arr] = np.array((0, 255, 255, 200)) # bgra

        # Create a QPixmap from the new array
        tempMaskPixmap = QtGui.QPixmap.fromImage(QtGui.QImage(new_arr.data, 
                                          new_arr.shape[1], 
                                          new_arr.shape[0], 
                                          QtGui.QImage.Format_ARGB32))
        
        self._tempMask.setPixmap(tempMaskPixmap)
        
        self._tempLabelObjects.append(mask)
    
    def drawMask(self):
        if self._tempLabelObjects:
            hull = getContours(self._currentMask)
            mask = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QPoint(*p) for p in hull.reshape(-1, 2)]))
            mask.setPen(QtGui.QPen(QtGui.QColor(255, 0, 0, 200), 5, QtCore.Qt.SolidLine))
            mask.setBrush(QtGui.QBrush(QtGui.QColor(255, 0, 0, 100), QtCore.Qt.SolidPattern))
            # mask.setSelected(True)
            self._tempLabelObjects.clear()
            self._tempMask.setPixmap(QtGui.QPixmap())
            self._currentMask[self._currentMask > 0] = 0
            self._scene.addItem(mask)
            self._labelObjects.append([mask, hull])

    def store(self):
        print('store')
        # print(base64.b64decode(self._cv2img).decode('utf-8'))
        labeljson = dict()
        labeljson["imageHeight"] = self._cv2img.shape[0]
        labeljson["imageWidth"] = self._cv2img.shape[1]
        labeljson["imagePath"] = None
        labeljson["imageData"] = base64.b64decode(self._cv2img)
        labeljson["version"] = "5.0.1" # opt
        labeljson["flags"] = dict() # opt
        shapes = []
        
        for shape in self._labelObjects:
            anno = dict()
            anno["label"] = "intersection"
            anno["points"] = shape[1].reshape(-1,2).tolist()
            anno["group_id"] = None
            anno["shape_type"] = "polygon"
            anno["flags"] = dict()
            shapes.append(anno)
        labeljson["shapes"] = shapes
        with open(os.path.splitext(self._imgPath)[0]+'.json', 'w') as f:
            json.dump(labeljson, f, indent=2)
    
    # def haveTempMask(self):
    #     return len(self._tempLabelObjects) != 0
    

# class Window(QtWidgets.QWidget):
#     def __init__(self):
#         super(Window, self).__init__()
#         self.viewer = PhotoViewer(self)
        
#         # Arrange layout
#         VBlayout = QtWidgets.QVBoxLayout(self)
#         VBlayout.addWidget(self.viewer)
#         # self.loadImage()

#     def loadImage(self, filename: str):
#         self.viewer.setPhoto(QtGui.QPixmap(filename))

#     def pixInfo(self):
#         self.viewer.toggleDragMode()



# if __name__ == '__main__':
#     import sys
#     app = QtWidgets.QApplication(sys.argv)
#     window = Window()
#     window.setGeometry(500, 300, 800, 600)
#     window.show()
#     sys.exit(app.exec_())