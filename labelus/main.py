import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QMainWindow, QListWidget, QListWidgetItem
# from PyQt5.QtGui import QResizeEvent
from PyQt5.QtCore import Qt

from canvas import Canvas
from filelist import FileList
from tools import Tools


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Create the QLabel instance
        self.filelist = FileList()
        self.filelist.itemDoubleClicked.connect(self.openFile)

        tools = Tools()
        print("tools", tools.getContentsMargins())
        tools.button1.clicked.connect(self.openFileDialog)
        tools.button2.clicked.connect(self.openFolderDialog)
        self.img = Canvas("")

        # Create a QHBoxLayout and add the button layout and label
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(tools)
        mainLayout.addWidget(self.img)
        mainLayout.addWidget(self.filelist)

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
        self.img.label.move(self.img.xx, self.img.yy)
        print('canvas size:', self.img.width(), 'x', self.img.height())
        print('canvas size:', self.img.label.width(), 'x', self.img.label.height())
        super().resizeEvent(event)

    def openFile(self, item):
        print(item.whatsThis())
        filename = item.whatsThis()
        self.img.path = filename
        self.img.update()


    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)", options=options)
        if fileName:
            
            # print(fileName)
            self.img.path = fileName
            # print('oepn canvas size:', self.img.width(), 'x', self.img.height())
            
            self.img.update()
            # pixmap = QPixmap(fileName)
            # self.label.setPixmap(pixmap)
    
    def openFolderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)
        filelist = []
        if folder:
            for file in os.listdir(folder):
                if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.bmp'):
                    filelist.append(os.path.join(folder, file))
        
                    item = QListWidgetItem(file)
                    item.setWhatsThis(os.path.join(folder, file))
                    self.filelist.addItem(item)
        print(filelist)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainpage = MainPage()
    sys.exit(app.exec_())