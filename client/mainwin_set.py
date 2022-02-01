import queue
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets
from mainwin import Ui_SpecArt_MainWindow
from specart_com import Com
from queue import Queue
import sys

class mainCom(Com):
    def __init__(self, mode, window):
        self.window = window

        return super().__init__(mode)

    def GUI_fresh(self):
        # Fresh winning process
        self.window.win_progressBar.value = int(self.player.money / self.totalPlayerMoney)
        
        # Fresh waiting order list
        table = self.window.sell_tableWidget
        table.setRowCount(0)
        table.clearContents()
        for item in self.buying.items:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, str(item[0]))     # Fill in price and number
            table.setItem(row, 1, str(item[1]))
            table.item(row, 0).setForeground(QBrush(QColor(0, 255, 0)))     # Set green color
            table.item(row, 1).setForeground(QBrush(QColor(0, 255, 0)))
            
        table = self.window.buy_tableWidget
        table.setRowCount(0)
        table.clearContents()
        for item in self.selling.items:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, str(item[0]))     # Fill in price and number
            table.setItem(row, 1, str(item[1]))
            table.item(row, 0).setForeground(QBrush(QColor(255, 0, 0)))     # Set red color
            table.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))

        # Fresh goods and money in status bar
        self.window.statusbar.showMessage(f'状态 # 金钱: {self.player.money} | 物资: {self.player.goods}')

        # Fresh price in LCD
        self.window.price_lcdNumber.intValue = self.price

    def GUI_newDeal(self, dir, price, num):
        # Red for positive buy (0)
        # Green for positive sell (1)
        table = self.window.deal_tableWidget
        row = table.rowCount()
        table.insertRow(row)

        # Fill in price and number
        table.setItem(row, 0, str(price))
        table.setItem(row, 1, str(num))

        # Set color
        if dir == 0:
            table.item(row, 0).setForeground(QBrush(QColor(255, 0, 0)))
            table.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))
        elif dir == 1:
            table.item(row, 0).setForeground(QBrush(QColor(0, 255, 0)))
            table.item(row, 1).setForeground(QBrush(QColor(0, 255, 0)))

    def GUI_msgbox(self, content):
        self.window.new_notice(content)

class mainWin(Ui_SpecArt_MainWindow, QMainWindow):
    newNotice = pyqtSignal()

    def __init__(self):
        super(mainWin, self).__init__()
        self.com = mainCom(1, self)
        self.setupUi(self)

        self.notice_que = Queue()

        # Set QTableWidget uneditable
        self.sell_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.buy_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.deal_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.com.notice('登录成功！等待服务器开始游戏...')

    def currentPriceShow(self):
        self.lcdNumber.setDigitCount(len(self.price))
        self.lcdNumber.display(self.price)

    def display_notice(self):
        if not self.notice_que.empty():
            msg = self.notice_que.get()
            QMessageBox.information(self.window, '提示', msg)
    
    def new_notice(self, content):
        self.notice_que.put(content)
        self.newNotice.emit()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())
