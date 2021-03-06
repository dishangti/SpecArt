# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwin.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SpecArt_MainWindow(object):
    def setupUi(self, SpecArt_MainWindow):
        SpecArt_MainWindow.setObjectName("SpecArt_MainWindow")
        SpecArt_MainWindow.resize(911, 563)
        self.centralwidget = QtWidgets.QWidget(SpecArt_MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.price_lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.price_lcdNumber.setGeometry(QtCore.QRect(300, 0, 361, 51))
        self.price_lcdNumber.setFrameShape(QtWidgets.QFrame.Box)
        self.price_lcdNumber.setDigitCount(14)
        self.price_lcdNumber.setProperty("value", 0.0)
        self.price_lcdNumber.setProperty("intValue", 0)
        self.price_lcdNumber.setObjectName("price_lcdNumber")
        self.timeChart_openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.timeChart_openGLWidget.setGeometry(QtCore.QRect(0, 0, 300, 191))
        self.timeChart_openGLWidget.setObjectName("timeChart_openGLWidget")
        self.win_progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.win_progressBar.setGeometry(QtCore.QRect(120, 504, 771, 16))
        self.win_progressBar.setStyleSheet("QProgressBar {\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"QProgressBar {\n"
"    min-height: 12px;\n"
"    max-height: 12px;\n"
"    border-radius: 6px;\n"
"}\n"
"QProgressBar::chunk {\n"
"    border-radius: 6px;\n"
"    background-color: #00B4A0;\n"
"}")
        self.win_progressBar.setProperty("value", 0)
        self.win_progressBar.setObjectName("win_progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 500, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(20, 330, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.price_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.price_lineEdit.setGeometry(QtCore.QRect(70, 330, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.price_lineEdit.setFont(font)
        self.price_lineEdit.setObjectName("price_lineEdit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(20, 390, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.num_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.num_lineEdit.setGeometry(QtCore.QRect(70, 390, 151, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.num_lineEdit.setFont(font)
        self.num_lineEdit.setObjectName("num_lineEdit")
        self.buy_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.buy_pushButton.setEnabled(False)
        self.buy_pushButton.setGeometry(QtCore.QRect(240, 320, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buy_pushButton.setFont(font)
        self.buy_pushButton.setObjectName("buy_pushButton")
        self.sell_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.sell_pushButton.setEnabled(False)
        self.sell_pushButton.setGeometry(QtCore.QRect(240, 380, 121, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.sell_pushButton.setFont(font)
        self.sell_pushButton.setObjectName("sell_pushButton")
        self.volumn_openGLWidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.volumn_openGLWidget.setGeometry(QtCore.QRect(0, 190, 300, 71))
        self.volumn_openGLWidget.setObjectName("volumn_openGLWidget")
        self.deal_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.deal_tableWidget.setGeometry(QtCore.QRect(370, 270, 281, 221))
        self.deal_tableWidget.setObjectName("deal_tableWidget")
        self.deal_tableWidget.setColumnCount(3)
        self.deal_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.deal_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.deal_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.deal_tableWidget.setHorizontalHeaderItem(2, item)
        self.deal_tableWidget.horizontalHeader().setVisible(True)
        self.deal_tableWidget.horizontalHeader().setDefaultSectionSize(89)
        self.deal_tableWidget.verticalHeader().setVisible(False)
        self.sell_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.sell_tableWidget.setGeometry(QtCore.QRect(300, 80, 181, 181))
        self.sell_tableWidget.setLineWidth(0)
        self.sell_tableWidget.setObjectName("sell_tableWidget")
        self.sell_tableWidget.setColumnCount(2)
        self.sell_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.sell_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.sell_tableWidget.setHorizontalHeaderItem(1, item)
        self.sell_tableWidget.horizontalHeader().setVisible(True)
        self.sell_tableWidget.horizontalHeader().setDefaultSectionSize(87)
        self.sell_tableWidget.verticalHeader().setVisible(False)
        self.buy_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.buy_tableWidget.setGeometry(QtCore.QRect(480, 80, 181, 181))
        self.buy_tableWidget.setObjectName("buy_tableWidget")
        self.buy_tableWidget.setColumnCount(2)
        self.buy_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.buy_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.buy_tableWidget.setHorizontalHeaderItem(1, item)
        self.buy_tableWidget.horizontalHeader().setDefaultSectionSize(87)
        self.buy_tableWidget.verticalHeader().setVisible(False)
        self.trans_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.trans_tableWidget.setGeometry(QtCore.QRect(660, 30, 241, 341))
        self.trans_tableWidget.setObjectName("trans_tableWidget")
        self.trans_tableWidget.setColumnCount(4)
        self.trans_tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.trans_tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.trans_tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.trans_tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.trans_tableWidget.setHorizontalHeaderItem(3, item)
        self.trans_tableWidget.horizontalHeader().setDefaultSectionSize(58)
        self.trans_tableWidget.verticalHeader().setVisible(False)
        self.back_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.back_pushButton.setEnabled(False)
        self.back_pushButton.setGeometry(QtCore.QRect(710, 380, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.back_pushButton.setFont(font)
        self.back_pushButton.setObjectName("back_pushButton")
        self.players_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.players_pushButton.setEnabled(False)
        self.players_pushButton.setGeometry(QtCore.QRect(710, 440, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.players_pushButton.setFont(font)
        self.players_pushButton.setObjectName("players_pushButton")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(310, 56, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(500, 57, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(320, 280, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(671, 8, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        SpecArt_MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(SpecArt_MainWindow)
        self.statusbar.setObjectName("statusbar")
        SpecArt_MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SpecArt_MainWindow)
        QtCore.QMetaObject.connectSlotsByName(SpecArt_MainWindow)

    def retranslateUi(self, SpecArt_MainWindow):
        _translate = QtCore.QCoreApplication.translate
        SpecArt_MainWindow.setWindowTitle(_translate("SpecArt_MainWindow", "SpecArt"))
        self.label.setText(_translate("SpecArt_MainWindow", "Winning Process"))
        self.label_2.setText(_translate("SpecArt_MainWindow", "Price"))
        self.label_3.setText(_translate("SpecArt_MainWindow", "Num"))
        self.buy_pushButton.setText(_translate("SpecArt_MainWindow", "Buy"))
        self.sell_pushButton.setText(_translate("SpecArt_MainWindow", "Sell"))
        item = self.deal_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SpecArt_MainWindow", "Price"))
        item = self.deal_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SpecArt_MainWindow", "Num"))
        item = self.deal_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("SpecArt_MainWindow", "Time"))
        item = self.sell_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SpecArt_MainWindow", "Price"))
        item = self.sell_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SpecArt_MainWindow", "Num"))
        item = self.buy_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SpecArt_MainWindow", "Price"))
        item = self.buy_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SpecArt_MainWindow", "Num"))
        item = self.trans_tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("SpecArt_MainWindow", "Dir"))
        item = self.trans_tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("SpecArt_MainWindow", "Price"))
        item = self.trans_tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("SpecArt_MainWindow", "Num"))
        item = self.trans_tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("SpecArt_MainWindow", "Time"))
        self.back_pushButton.setText(_translate("SpecArt_MainWindow", "Withdraw"))
        self.players_pushButton.setText(_translate("SpecArt_MainWindow", "Player List"))
        self.label_4.setText(_translate("SpecArt_MainWindow", "Selling"))
        self.label_5.setText(_translate("SpecArt_MainWindow", "Buying"))
        self.label_6.setText(_translate("SpecArt_MainWindow", "Deal"))
        self.label_7.setText(_translate("SpecArt_MainWindow", "My Transections"))
