# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'welcome.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.lan_pushButton = QtWidgets.QPushButton(Form)
        self.lan_pushButton.setGeometry(QtCore.QRect(270, 150, 101, 31))
        self.lan_pushButton.setObjectName("lan_pushButton")
        self.teach_pushButton = QtWidgets.QPushButton(Form)
        self.teach_pushButton.setEnabled(False)
        self.teach_pushButton.setGeometry(QtCore.QRect(270, 190, 101, 31))
        self.teach_pushButton.setObjectName("teach_pushButton")
        self.about_pushButton = QtWidgets.QPushButton(Form)
        self.about_pushButton.setGeometry(QtCore.QRect(270, 230, 101, 31))
        self.about_pushButton.setObjectName("about_pushButton")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 20, 231, 61))
        font = QtGui.QFont()
        font.setFamily("Ink Free")
        font.setPointSize(45)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setOpenExternalLinks(False)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(60, 100, 321, 21))
        font = QtGui.QFont()
        font.setFamily("Ink Free")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(0, 0, 401, 301))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap(":/background/welcome_background.jpg"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.label_3.raise_()
        self.lan_pushButton.raise_()
        self.teach_pushButton.raise_()
        self.about_pushButton.raise_()
        self.label.raise_()
        self.label_2.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "SpecArt-Welcome"))
        self.lan_pushButton.setText(_translate("Form", "Online Game"))
        self.teach_pushButton.setText(_translate("Form", "Local Teaching"))
        self.about_pushButton.setText(_translate("Form", "About"))
        self.label.setText(_translate("Form", "SpecArt"))
        self.label_2.setText(_translate("Form", "\"Speculation is as old as the hills\""))
import welcome_background_rc
