from PyQt5.QtWidgets import QMainWindow
from login import Ui_MainWindow
 
class mainWin(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(mainWin, self).__init__()

        self.setupUi(self)