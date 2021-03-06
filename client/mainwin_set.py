from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtGui import QColor, QBrush
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtWidgets, QtGui
from mainwin import Ui_SpecArt_MainWindow
from specart_com import Com
from queue import Queue
import sys
import playerlist_set
from time import localtime

class GUICom(Com):
    def __init__(self, mode, window):
        super().__init__(mode)
        self.window = window

    def GUI_newDeal(self, dir, price, num, deal_time):
        self.window.new_deal(dir, price, num, deal_time)

    def GUI_msgbox(self, content):
        self.window.new_notice(content)

class mainWin(Ui_SpecArt_MainWindow, QMainWindow):
    newNotice = pyqtSignal()                # Display notices in queue
    newDeal = pyqtSignal()                  # Display deals in queue
    beginGame = pyqtSignal()
    freshWinProcessBar = pyqtSignal()
    freshBuyTableWidget = pyqtSignal()
    freshSellTableWidget = pyqtSignal()
    freshTransTableWidget = pyqtSignal()
    freshStatusBar = pyqtSignal()
    freshLCD = pyqtSignal()
    updatePlayer = pyqtSignal()             # Fresh the total num of players

    def __init__(self):
        super(Ui_SpecArt_MainWindow, self).__init__()
        self.com = GUICom(1, self)
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
        self.trans_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

        # Fix and set column widths in QTableWidget
        self.buy_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.sell_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.deal_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.trans_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Fixed)
        self.trans_tableWidget.setColumnWidth(0, 40)    # Direction
        self.trans_tableWidget.setColumnWidth(1, 66)    # Price
        self.trans_tableWidget.setColumnWidth(2, 66)    # Number
        self.trans_tableWidget.setColumnWidth(3, 65)    # Time

        # Set QTableWidget select row only
        self.trans_tableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.trans_tableWidget.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

        # Set slots for signals
        self.buy_pushButton.clicked.connect(self.__buy_pushButton_clicked)
        self.sell_pushButton.clicked.connect(self.__sell_pushButton_clicked)
        self.players_pushButton.clicked.connect(self.__players_pushButton_clicked)
        self.back_pushButton.clicked.connect(self.__back_pushButton_clicked)
        self.buy_tableWidget.doubleClicked.connect(self.__buy_tableWidget_doubleClicked)      # Set price automatically when double clicking
        self.sell_tableWidget.doubleClicked.connect(self.__sell_tableWidget_doubleClicked)

        self.newNotice.connect(self.__display_notice)
        self.newDeal.connect(self.__display_deal)
        self.beginGame.connect(self.__begin_game)
        self.freshWinProcessBar.connect(self.__fresh_winProcessBar)
        self.freshBuyTableWidget.connect(self.__fresh_buyTableWidget)
        self.freshSellTableWidget.connect(self.__fresh_sellTableWidget)
        self.freshTransTableWidget.connect(self.__fresh_transTableWidget)
        self.freshStatusBar.connect(self.__fresh_StatusBar)
        self.freshLCD.connect(self.__fresh_LCD)
        self.updatePlayer.connect(self.__update_player)

        # Fix the window size
        self.setFixedSize(self.width(), self.height())

    def __buy_pushButton_clicked(self):
        if self.price_lineEdit.text() == "" or self.num_lineEdit.text() == "":
            return
        price = int(self.price_lineEdit.text())
        num = int(self.num_lineEdit.text())
        self.com.buy(num, price)

    def __sell_pushButton_clicked(self):
        if self.price_lineEdit.text() == "" or self.num_lineEdit.text() == "":
            return
        price = int(self.price_lineEdit.text())
        num = int(self.num_lineEdit.text())
        self.com.sell(num, price)

    def __players_pushButton_clicked(self):
        self.window = playerlist_set.mianWidget(self.com.playerList)
        self.window.show()

    def __back_pushButton_clicked(self):
        trans = self.com.player.transaction
        select_items = self.trans_tableWidget.selectedItems()
        if len(select_items) == 0: return
        if select_items[0].text() == "Sell":
            dir = 'sell'
        elif select_items[0].text() == "Buy":
            dir = 'buy'
        price = int(select_items[1].text())
        num = int(select_items[2].text())
        tran_time = select_items[3].text()
        for tran in trans.values():
            precise_tran_time = localtime(float(tran[3]))[3:6]
            precise_time_str = str(precise_tran_time[0]).zfill(2) + ":" + str(precise_tran_time[1]).zfill(2) + ":" + str(precise_tran_time[2]).zfill(2)
            # Find and delete a order with the same hour, min and sec
            if tran[0] == dir and int(tran[1]) == num and int(tran[2]) == price and precise_time_str == tran_time:
                if dir == 'sell':
                    self.com.backsell(int(num), int(price), tran[3])
                elif dir == 'buy':
                    self.com.backbuy(int(num), int(price), tran[3])
                break

    def __buy_tableWidget_doubleClicked(self):
        select_items = self.buy_tableWidget.selectedItems()
        if len(select_items) == 0: return
        col = select_items[0].column()
        if col == 0:
            self.price_lineEdit.setText(select_items[0].text())

    def __sell_tableWidget_doubleClicked(self):
        select_items = self.sell_tableWidget.selectedItems()
        if len(select_items) == 0: return
        col = select_items[0].column()
        if col == 0:
            self.price_lineEdit.setText(select_items[0].text())

    def __begin_game(self):
        # Judge whether game has begun
        if self.com.beginTime != "":
            self.buy_pushButton.setEnabled(True)
            self.sell_pushButton.setEnabled(True)
            self.back_pushButton.setEnabled(True)
            self.players_pushButton.setEnabled(True)

    def __update_player(self):
        self.com.totalPlayerMoney = len(self.com.playerList) * self.com.initMoney

    def __fresh_winProcessBar(self):
        if self.com.totalPlayerMoney != 0:
            self.win_progressBar.setValue(min(int(self.com.player.money / (self.com.totalPlayerMoney * 0.6) * 100), 100))

    def __fresh_buyTableWidget(self):
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
        table.scrollToTop()

    def __fresh_sellTableWidget(self):
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
        table.scrollToBottom()

    def __fresh_transTableWidget(self):
        trans = list(self.com.player.transaction.values())
        trans.sort(key=lambda x: x[2])
        trans.reverse()
        table = self.trans_tableWidget
        table.setRowCount(0)
        table.clearContents()
        for tran in trans:
            dir = tran[0]
            num = tran[1]
            price = tran[2]
            tran_time = localtime(float(tran[3]))[3:6]
            time_str = str(tran_time[0]).zfill(2) + ":" + str(tran_time[1]).zfill(2) + ":" + str(tran_time[2]).zfill(2)

            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 1, QTableWidgetItem(str(price)))     # Fill in price and number
            table.setItem(row, 2, QTableWidgetItem(str(num)))
            table.setItem(row, 3, QTableWidgetItem(time_str))
            if dir == 'sell':
                table.setItem(row, 0, QTableWidgetItem('Sell'))
                table.item(row, 0).setForeground(QBrush(QColor(0, 255, 0)))     # Set green color
                table.item(row, 1).setForeground(QBrush(QColor(0, 255, 0)))
                table.item(row, 2).setForeground(QBrush(QColor(0, 255, 0)))
                table.item(row, 3).setForeground(QBrush(QColor(0, 255, 0)))
            elif dir == 'buy':
                table.setItem(row, 0, QTableWidgetItem('Buy'))
                table.item(row, 0).setForeground(QBrush(QColor(255, 0, 0)))     # Set red color
                table.item(row, 1).setForeground(QBrush(QColor(255, 0, 0)))
                table.item(row, 2).setForeground(QBrush(QColor(255, 0, 0)))
                table.item(row, 3).setForeground(QBrush(QColor(255, 0, 0)))

    def __fresh_StatusBar(self):
        # Fresh goods and money in status bar
        self.statusbar.showMessage(f'Status # Money: {self.com.player.money} | Goods: {self.com.player.goods}')

    def __fresh_LCD(self):
        # Fresh price in LCD
        self.price_lcdNumber.display(self.com.price)

    def __display_notice(self):
        if not self.notice_que.empty():
            msg = self.notice_que.get()
            QMessageBox.information(self, 'Notice', msg)
    
    def __add_deal_item(self, dir, price, num, deal_time):
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

    def __display_deal(self):
        if not self.deal_que.empty():
            dir, price, num, deal_time = self.deal_que.get()
            self.__add_deal_item(dir, price, num, deal_time)

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
