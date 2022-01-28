from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtCore, QtWidgets
from mainwin import Ui_SpecArt_MainWindow
from specart_com import Com
import sys

class mainCom(Com):
    def __init__(self, mode, window):
        self.window = window

        return super().__init__(mode)

    def GUI_msgbox(self, content):
        QMessageBox.information(self.window, '提示', content)

class mainWin(Ui_SpecArt_MainWindow, QMainWindow):
    def __init__(self):
        super(mainWin, self).__init__()
        self.com = mainCom(1, self)
        self.setupUi(self)

        self.price = None
        self.buying = None
        self.selling = None
        self.winning_status = None

    def currentPriceShow(self):
        self.lcdNumber.setDigitCount(len(self.price))
        self.lcdNumber.display(self.price)

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())