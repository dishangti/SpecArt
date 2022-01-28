from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtCore, QtWidgets
from mainwin import Ui_SpecArt_MainWindow
from specart_com import Com
import sys

class mainWin(Ui_SpecArt_MainWindow, QMainWindow):
    def __init__(self):
        super(mainWin, self).__init__()
        self.com = mainCom(1, self)
        self.setupUi(self)

        self.playernum = 0

    def currentPriceShow(self):
        self.lcdNumber.setDigitCount(len(self.price))
        self.lcdNumber.display(self.price)

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())

class mainCom(Com):
    def __init__(self, mode, window:mainWin):
        self.window = window

        return super().__init__(mode)

    def GUI_msgbox(self, content):
        QMessageBox.information(self.window, '提示', content)

    def GUI_fresh(self):
        # Fresh winning process
        self.window.win_progressBar.value = int(self.player.money / self.totalPlayerMoney )
        
        # Fresh waiting order list

        # Fresh goods and money in status bar
        self.window.statusbar.showMessage(f'状态 | 金钱: {self.player.money} | 物资: {self.player.goods}')

    def GUI_newDeal(self, dir, price, num):
        pass