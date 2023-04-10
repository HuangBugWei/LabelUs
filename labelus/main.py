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
        self.filelist = FileList()
        self.tools = Tools()
        self.canvas = Canvas()

        self.initUI()

    def initUI(self):

        self.filelist.itemDoubleClicked.connect(self.openFile)

        self.tools.button1.clicked.connect(self.openFileDialog)
        self.tools.button2.clicked.connect(self.openFolderDialog)

        # Create a QHBoxLayout and add the button layout and label
        mainLayout = QHBoxLayout()
        mainLayout.addLayout(self.tools)
        mainLayout.addWidget(self.canvas)
        mainLayout.addWidget(self.filelist)
        
        # Set the main layout of the window
        self.setLayout(mainLayout)
        self.setGeometry(100, 100, 1620, 880)
        self.setMinimumSize(1080, 720)
        self.setWindowTitle('LabelUs')
        self.show()

    def resizeEvent(self, event):
        self.canvas.yy = self.canvas.height() // 2 - self.canvas.label.height() // 2
        self.canvas.xx = self.canvas.width() // 2 - self.canvas.label.width() // 2
        self.canvas.label.move(self.canvas.xx, self.canvas.yy)
        super().resizeEvent(event)

    def openFile(self, item):
        print(item.whatsThis())
        filename = item.whatsThis()
        self.canvas.path = filename
        self.canvas.update()


    def openFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.xpm *.jpg *.jpeg *.bmp *.gif)", options=options)
        if fileName:
            
            self.canvas.path = fileName
            self.canvas.update()
    
    def openFolderDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ShowDirsOnly
        folder = QFileDialog.getExistingDirectory(self, "Select Directory", "", options=options)

        if folder:
            for file in os.listdir(folder):
                if file.endswith('.jpg') or file.endswith('.jpeg') or file.endswith('.png') or file.endswith('.bmp'):
                    item = QListWidgetItem(file)
                    item.setWhatsThis(os.path.join(folder, file))
                    self.filelist.addItem(item)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainpage = MainPage()
    sys.exit(app.exec_())
