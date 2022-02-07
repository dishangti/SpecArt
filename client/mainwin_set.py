from select import select
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets, QtGui
from mainwin import Ui_SpecArt_MainWindow
from specart_com import Com
from queue import Queue
import sys
import playerlist_set

class mainCom(Com):
    def __init__(self, mode, window):
        self.window = window

        return super().__init__(mode)

    def GUI_fresh(self):
        self.window.fresh_GUI()

    def GUI_newDeal(self, dir, price, num, deal_time):
        self.window.new_deal(dir, price, num, deal_time)

    def GUI_msgbox(self, content):
        self.window.new_notice(content)

class mainWin(Ui_SpecArt_MainWindow, QMainWindow):
    newNotice = pyqtSignal()
    newData = pyqtSignal()
    newDeal = pyqtSignal()
    freshWin = pyqtSignal()

    def __init__(self):
        super(Ui_SpecArt_MainWindow, self).__init__()
        self.com = mainCom(1, self)
        self.setupUi(self)

        self.notice_que = Queue()
        self.deal_que = Queue()

        # Set price and num lineEdit for integer only
        self.price_lineEdit.setValidator(QtGui.QIntValidator())
        self.num_lineEdit.setValidator(QtGui.QIntValidator())

        # Set QTableWidget uneditable
        self.sell_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.buy_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.deal_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.com.notice('登录成功！等待服务器开始游戏...')

        # Set slots for signals
        self.buy_pushButton.clicked.connect(self.buy_pushButton_clicked)
        self.sell_pushButton.clicked.connect(self.sell_pushButton_clicked)
        self.players_pushButton.clicked.connect(self.players_pushButton_clicked)
        self.buy_tableWidget.doubleClicked.connect(self.buy_tableWidget_doubleClicked)      # Set price automatically when double clicking
        self.sell_tableWidget.doubleClicked.connect(self.sell_tableWidget_doubleClicked)
        self.newNotice.connect(self.display_notice)
        self.newData.connect(self.fresh_GUI)
        self.newDeal.connect(self.display_deal)
        self.freshWin.connect(self.fresh_win_process)

    def buy_pushButton_clicked(self):
        if self.price_lineEdit.text() == "" or self.num_lineEdit.text() == "":
            return
        price = int(self.price_lineEdit.text())
        num = int(self.num_lineEdit.text())
        self.com.buy(num, price)

    def sell_pushButton_clicked(self):
        if self.price_lineEdit.text() == "" or self.num_lineEdit.text() == "":
            return
        price = int(self.price_lineEdit.text())
        num = int(self.num_lineEdit.text())
        self.com.sell(num, price)

    def players_pushButton_clicked(self):
        self.window = playerlist_set.mianWidget(self.com.playerList)
        self.window.show()

    def buy_tableWidget_doubleClicked(self):
        
        select_items = self.buy_tableWidget.selectedItems()
        if len(select_items) == 0: return
        col = self.buy_tableWidget.selectedItems()[0].column()
        if col == 0:
            self.price_lineEdit.setText(select_items[0].text())

    def sell_tableWidget_doubleClicked(self):
        select_items = self.sell_tableWidget.selectedItems()
        if len(select_items) == 0: return
        col = self.sell_tableWidget.selectedItems()[0].column()
        if col == 0:
            self.price_lineEdit.setText(select_items[0].text())

    def fresh_win_process(self):
        self.win_progressBar.setValue(max(int(self.com.player.money / (self.com.totalPlayerMoney * 0.6) * 100), 100))

    def display_notice(self):
        if not self.notice_que.empty():
            msg = self.notice_que.get()
            QMessageBox.information(self, '提示', msg)
    
    def add_deal_item(self, dir, price, num, deal_time):
        # Red for positive buy (0)
        # Green for positive sell (1)
        table = self.deal_tableWidget
        row = table.rowCount()
        table.insertRow(row)

        # Fill in price, number and time
        table.setItem(row, 0, QTableWidgetItem(str(price)))
        table.setItem(row, 1, QTableWidgetItem(str(num)))
        time_str = str(deal_time[0]).zfill(2) + ":" + str(deal_time[1]).zfill(2) + ":" + str(deal_time[2]).zfill(2)
        table.setItem(row, 2, QTableWidgetItem(time_str))

        # Set color
        if dir == 0:
            table.item(row, 0).setForeground(QBrush(QColor(255, 0, 0)))
            table.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))
            table.item(row, 2).setForeground(QBrush(QColor(255, 0, 0)))
        elif dir == 1:
            table.item(row, 0).setForeground(QBrush(QColor(0, 255, 0)))
            table.item(row, 1).setForeground(QBrush(QColor(0, 255, 0)))
            table.item(row, 2).setForeground(QBrush(QColor(0, 255, 0)))

        table.scrollToBottom()

    def display_deal(self):
        if not self.deal_que.empty():
            dir, price, num, deal_time = self.deal_que.get()
            self.add_deal_item(dir, price, num, deal_time)

    def fresh_GUI(self):
        # Judge whether game has begun
        if self.com.beginTime != "":
            self.buy_pushButton.setEnabled(True)
            self.sell_pushButton.setEnabled(True)
            self.back_pushButton.setEnabled(True)
            self.players_pushButton.setEnabled(True)
            self.com.totalPlayerMoney = len(self.com.playerList) * self.com.initMoney

        # Fresh winning process
        if self.com.totalPlayerMoney != 0:
            self.freshWin.emit()

        # Fresh waiting order list
        table = self.buy_tableWidget
        table.setRowCount(0)
        table.clearContents()
        for item in self.com.buying.get_order():
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(item[0])))     # Fill in price, number
            table.setItem(row, 1, QTableWidgetItem(str(item[1])))
            table.item(row, 0).setForeground(QBrush(QColor(255, 0, 0)))     # Set red color
            table.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))
        table.scrollToBottom()
            
        table = self.sell_tableWidget
        table.setRowCount(0)
        table.clearContents()
        for item in self.com.selling.get_order():
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(item[0])))     # Fill in price and number
            table.setItem(row, 1, QTableWidgetItem(str(item[1])))
            table.item(row, 0).setForeground(QBrush(QColor(0, 255, 0)))     # Set green color
            table.item(row, 1).setForeground(QBrush(QColor(0, 255, 0)))
        table.scrollToTop()

        # Fresh goods and money in status bar
        self.statusbar.showMessage(f'状态 # 金钱: {self.com.player.money} | 物资: {self.com.player.goods}')

        # Fresh price in LCD
        self.price_lcdNumber.display(self.com.price)

    def new_notice(self, content):
        self.notice_que.put(content)
        self.newNotice.emit()

    def new_deal(self, dir, price, num, deal_time):
        self.deal_que.put((dir, price, num, deal_time))
        self.newDeal.emit()    

    def new_data(self):
        self.newData.emit()

if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    ui = mainWin()
    ui.show()
    sys.exit(app.exec_())
