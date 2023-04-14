from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QPoint, QPointF, QEvent
from utils import *
import cv2, os, json
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
        self._folder = None
        self._colorPlate = [QtGui.QColor(255,0,0), 
                            QtGui.QColor(0,255,0), 
                            QtGui.QColor(0,0,255), 
                            QtGui.QColor(255,255,0),
                            QtGui.QColor(0,255,255),
                            QtGui.QColor(255,0,255)]
        self._labelList = None
        self._labelCls = None
        
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setStyleSheet("background:transparent")
        # self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        shortcutUndo = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self)
        shortcutUndo.activated.connect(self.undo)

        shortcutStore = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+S"), self)
        shortcutStore.activated.connect(self.storeJson)

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
    
    def setLabelList(self, labellist):
        self._labelList = labellist
        self._labelList.clear()
        for mask, _, classname  in self._labelObjects:
            item = QtWidgets.QListWidgetItem(classname)
            # item.setData(0, mask)
            self._labelList.addItem(item)


    
    def setLabelCls(self, labelcls):
        self._labelCls = labelcls
        # self._labelCls.clearList()
        

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        if pixmap:
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._imgPath = os.path.basename(pixmap)
            self._folder = os.path.dirname(pixmap)
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
            self._scene.removeItem(it[0])
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
                factor = 0.85
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
            self._labelList.takeItem(len(self._labelObjects))
            self._scene.removeItem(it[0])
            del it
        

    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:

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
        arr = np.transpose(mask, (2, 0, 1))[0] > 0
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
    
    def drawMask(self, hull=None, clsName=None, order=None):
        if self._tempLabelObjects and not hull:
            hull = getContours(self._currentMask).reshape(-1, 2).tolist()
        if not hull:
            return
        if self._tempLabelObjects and not clsName:
            clsName = self._labelCls.getCurrent()
            if not clsName:
                return
        if self._tempLabelObjects and not order:
            order = self._labelCls.getOrder(clsName)
        

        
        mask = QtWidgets.QGraphicsPolygonItem(QtGui.QPolygonF([QPoint(*p) for p in hull]))
        while (order >= len(self._colorPlate)):
            color = tuple(np.random.randint(256, size=3))
            self._colorPlate.append(QtGui.QColor(*color))
        tempcolor = self._colorPlate[order]
        tempcolor.setAlpha(240)
        mask.setPen(QtGui.QPen(tempcolor, 5, QtCore.Qt.SolidLine))
        tempcolor.setAlpha(165)
        mask.setBrush(QtGui.QBrush(tempcolor, QtCore.Qt.SolidPattern))
        # mask.setSelected(True)
        self._tempLabelObjects.clear()
        self._tempMask.setPixmap(QtGui.QPixmap())
        self._currentMask[self._currentMask > 0] = 0
        self._scene.addItem(mask)
        self._labelObjects.append([mask, hull, clsName])
        
        if self._labelList is not None:
            self._labelList.addItem(clsName)
    

    def storeJson(self):
        print('store')
        # print(base64.b64decode(self._cv2img).decode('utf-8'))
        labeljson = dict()
        labeljson["imageHeight"] = self._cv2img.shape[0]
        labeljson["imageWidth"] = self._cv2img.shape[1]
        labeljson["imagePath"] = self._imgPath
        labeljson["imageData"] = None
        labeljson["version"] = "5.0.1" # opt
        labeljson["flags"] = dict() # opt
        shapes = []

        for shape in self._labelObjects:
            anno = dict()
            anno["label"] = shape[2]
            anno["points"] = shape[1]
            anno["group_id"] = None
            anno["shape_type"] = "polygon"
            anno["flags"] = dict()
            shapes.append(anno)
        labeljson["shapes"] = shapes

        jsonname = os.path.splitext(self._imgPath)[0]+'.json' 
        with open(os.path.join(self._folder, jsonname), 'w') as f:
            json.dump(labeljson, f, ensure_ascii=False, indent=2)
    
    def loadJson(self):
        print("load")
        path = os.path.join(self._folder,
                            os.path.splitext(self._imgPath)[0]+'.json')
        
        if os.path.isfile(path):
            with open(path, "r") as f:
                data = json.load(f)
                for anno in data["shapes"]:
                    hull = anno["points"]
                    clsName = anno["label"]
                    self._labelCls.addItem(clsName)
                    order = self._labelCls.getOrder(clsName)
                    self.drawMask(hull, clsName, order)
        else:
            print("No json file")
    
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