import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QMainWindow, QListWidget, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from canvas import Canvas
from filelist import FileList
from tools import Tools
from graphic import *
from labelclass import *
import numpy as np

class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.labelist = FileList()
        self.filelist = FileList()
        self.labelcls = MyWidget()
        self.tools = Tools()
        # self.canvas = Canvas()
        self.viewer = PhotoViewer(self)

        self.initUI()

    def initUI(self):

        self.filelist.itemDoubleClicked.connect(self.openFile)
        self.labelist.itemDoubleClicked.connect(self.pp)
        self.tools.button1.clicked.connect(self.openFileDialog)
        self.tools.button2.clicked.connect(self.openFolderDialog)


        # Create a QHBoxLayout and add the button layout and label
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.labelcls)
        rightLayout.addWidget(self.labelist)
        rightLayout.addWidget(self.filelist)
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(self.tools)
        mainLayout.addWidget(self.viewer)
        mainLayout.addLayout(rightLayout)
        
        # Set the main layout of the window
        self.setLayout(mainLayout)
        self.setGeometry(100, 100, 1620, 880)
        self.setMinimumSize(1080, 720)
        self.setWindowTitle('LabelUs')
        self.keyPressEvent = self.handleKeyPressEvent
        self.show()

    def openFile(self, item):
        print(item.whatsThis())
        fileName = item.whatsThis()
        haveJson = item.checkState()
        self.viewer.setPhoto(fileName)
        self.viewer.setLabelCls(self.labelcls)
        if haveJson:
            self.viewer.loadJson()
        self.viewer.setLabelList(self.labelist)

    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)", options=options)
        if fileName:
            # self.win.loadImage(fileName)
            self.viewer.setPhoto(fileName)
            self.viewer.setLabelCls(self.labelcls)
            self.viewer.loadJson()
            self.viewer.setLabelList(self.labelist)
            
            print(fileName)
    
    def openFolderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)

        if folder:
            self.filelist.clear()
            for file in os.listdir(folder):
                if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.bmp'):
                    item = QListWidgetItem(file)
                    item.setWhatsThis(os.path.join(folder, file))
                    jsonfile = os.path.splitext(file)[0] + ".json"
                    if os.path.isfile(os.path.join(folder, jsonfile)):
                        item.setCheckState(Qt.Checked)
                    else:
                        item.setCheckState(Qt.Unchecked)
                    # item.setCheckState(Qt.PartiallyChecked)
                    self.filelist.addItem(item)
    
    def handleKeyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            print("key A")
            self.viewer.undo()
        elif event.key() == Qt.Key_S:
            print("Key S")
            self.viewer.drawMask()

        # else:
        super().keyPressEvent(event)
    def pp(self, item):
        print(self.labelist.row(item))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainpage = MainPage()
    sys.exit(app.exec_())
