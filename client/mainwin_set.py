from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
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
        self.window.fresh_GUI()

    def GUI_newDeal(self, dir, price, num):
        self.window.new_deal(dir, price, num)

    def GUI_msgbox(self, content):
        self.window.new_notice(content)

class mainWin(Ui_SpecArt_MainWindow, QMainWindow):
    newNotice = pyqtSignal()
    newData = pyqtSignal()
    newDeal = pyqtSignal()

    def __init__(self):
        super(Ui_SpecArt_MainWindow, self).__init__()
        self.com = mainCom(1, self)
        self.setupUi(self)

        self.notice_que = Queue()
        self.deal_que = Queue()

        # Set QTableWidget uneditable
        self.sell_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.buy_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.deal_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.com.notice('登录成功！等待服务器开始游戏...')

        # Set slots for signals
        self.newNotice.connect(self.display_notice)
        self.newData.connect(self.fresh_GUI)
        self.newDeal.connect(self.display_deal)

    # def currentPriceShow(self):
    #     self.price_lcdNumber.setDigitCount(len(self.price))
    #     self.price_lcdNumber.display(self.price)

    def display_notice(self):
        if not self.notice_que.empty():
            msg = self.notice_que.get()
            QMessageBox.information(self, '提示', msg)
    
    def add_deal_item(self, dir, price, num):
        # Red for positive buy (0)
        # Green for positive sell (1)
        table = self.deal_tableWidget
        row = table.rowCount()
        table.insertRow(row)

        # Fill in price and number
        table.setItem(row, 0, QTableWidgetItem(str(price)))
        table.setItem(row, 1, QTableWidgetItem(str(num)))

        # Set color
        if dir == 0:
            table.item(row, 0).setForeground(QBrush(QColor(255, 0, 0)))
            table.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))
        elif dir == 1:
            table.item(row, 0).setForeground(QBrush(QColor(0, 255, 0)))
            table.item(row, 1).setForeground(QBrush(QColor(0, 255, 0)))

    def display_deal(self):
        if not self.deal_que.empty():
            dir, price, num = self.deal_que.get()
            self.add_deal_item(dir, price, num)

    def fresh_GUI(self):
        # Fresh winning process
        if self.com.totalPlayerMoney != 0:
            self.win_progressBar.value = int(self.com.player.money / (self.com.totalPlayerMoney * 0.6))

        # Fresh waiting order list
        table = self.buy_tableWidget
        table.setRowCount(0)
        table.clearContents()
        for item in self.com.buying.ord_lst:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(item[0])))     # Fill in price and number
            table.setItem(row, 1, QTableWidgetItem(str(item[1])))
            table.item(row, 0).setForeground(QBrush(QColor(255, 0, 0)))     # Set red color
            table.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))

            
        table = self.sell_tableWidget
        table.setRowCount(0)
        table.clearContents()
        for item in self.com.selling.ord_lst:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(item[0])))     # Fill in price and number
            table.setItem(row, 1, QTableWidgetItem(str(item[1])))
            table.item(row, 0).setForeground(QBrush(QColor(0, 255, 0)))     # Set green color
            table.item(row, 1).setForeground(QBrush(QColor(0, 255, 0)))

        # Fresh goods and money in status bar
        self.statusbar.showMessage(f'状态 # 金钱: {self.com.player.money} | 物资: {self.com.player.goods}')

        # Fresh price in LCD
        self.price_lcdNumber.display(self.com.price)

    def new_notice(self, content):
        self.notice_que.put(content)
        self.newNotice.emit()

    def new_deal(self, dir, price, num):
        self.deal_que.put((dir, price, num))
        self.newDeal.emit()    

    def new_data(self):
        self.newData.emit()

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())
