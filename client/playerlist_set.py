from PyQt5.QtWidgets import QWidget, QTableWidgetItem
from PyQt5.QtGui import QColor, QBrush
from playerlist import Ui_PlayerList_Dialog
 
class mianWidget(QWidget, Ui_PlayerList_Dialog):
    def __init__(self, playerList,parent=None):
        super(mianWidget, self).__init__()

        self.setupUi(self)
        self.close_pushButton.clicked.connect(self.close_pushButton_clicked)

        table = self.playerList_tableWidget
        for player in playerList:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(player[1])))     # Fill in price and number
            table.setItem(row, 1, QTableWidgetItem(str(player[0])))

    def close_pushButton_clicked(self):
        self.close()