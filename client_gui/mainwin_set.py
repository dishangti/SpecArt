from PyQt5.QtWidgets import QMainWindow
from mainwin import Ui_SpecArt_MainWindow

class mainWin(Ui_SpecArt_MainWindow, QMainWindow):
    def __init__(self):
        super(mainWin, self).__init__()

        self.price = None
        self.buying = None
        self.selling = None
        self.winning_status = None

    def currentPriceShow(self):
        self.lcdNumber.setDigitCount(len(self.price))
        self.lcdNumber.display(self.price)