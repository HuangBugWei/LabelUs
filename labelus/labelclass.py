import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget, QLineEdit, QDialog, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class InputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Enter Text')
        self.text_edit = QLineEdit(self)
        self.button_ok = QPushButton('OK', self)
        self.button_ok.clicked.connect(self.accept)
        layout = QVBoxLayout(self)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button_ok)

    def getText(self):
        return self.text_edit.text()

class ErrorDialog(QMessageBox):
    def __init__(self, message):
        # super().__init__(message)
        self.information(None, "error", message)


class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Create the buttons and the list widget
        self.setAcceptDrops(True)
        self.button1 = QPushButton('add class', self)
        self.button1.clicked.connect(self.showDialog)
        self.button2 = QPushButton('del class', self)
        self.button2.clicked.connect(self.deleteItem)
        self.list_widget = QListWidget(self)
        self.setMinimumWidth(140)
        self.setMaximumWidth(240)

        # Create the layout and add the widgets to it
        layout = QVBoxLayout(self)
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.button1)
        hlayout.addWidget(self.button2)

        layout.addLayout(hlayout)
        layout.addWidget(self.list_widget)
        hlayout.setContentsMargins(0,0,0,0)
        layout.setContentsMargins(0,0,0,0)
        

    def showDialog(self):
        dialog = InputDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            text = dialog.getText()
            self.addItem(text)
    
    def addItem(self, text):
        # List[QListWidgetItem]
        candidate = self.list_widget.findItems(text, Qt.MatchExactly)
        if candidate:
            print("class exist")
        else:
            self.list_widget.addItem(text)

    def clearList(self):
        self.list_widget.clear()

    def deleteItem(self):
        # Get currently selected item and remove it from list widget
        item = self.list_widget.currentItem()
        if item:
            self.list_widget.takeItem(self.list_widget.row(item))
    
    def getCurrent(self):
        item = self.list_widget.currentItem()
        if item:
            return item.text()
        else:
            QMessageBox.warning(None, 'Error', 'You should choose input label class.')
            return None

    def getOrder(self, text):
        candidate = self.list_widget.findItems(text, Qt.MatchExactly)
        return self.list_widget.row(candidate[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    widget = MyWidget()
    widget.show()
    sys.exit(app.exec_())
