from PyQt5.QtWidgets import QWidget, QMessageBox
from welcome import Ui_Form
from specart_com import Com
import login_set
 
class mainWin(QWidget, Ui_Form):
    def __init__(self,parent=None):
        super(mainWin, self).__init__()

        self.setupUi(self)
        self.lan_pushButton.clicked.connect(self.lan_pushButton_clicked)
        self.teach_pushButton.clicked.connect(self.teach_pushButton_clicked)
        self.about_pushButton.clicked.connect(self.about_pushButton_clicked)

        self.setFixedSize(self.width(), self.height())

    def lan_pushButton_clicked(self):
        self.ui = login_set.mainWin()
        self.ui.show()
        self.close()

    def teach_pushButton_clicked(self):
        pass

    def about_pushButton_clicked(self):
        info = 'SpecArt ' + Com.VERSION + '.' + '<br>' + 'See <a href=https://github.com/dishangti/SpecArt>https://github.com/dishangti/SpecArt</a>.'
        QMessageBox.information(self, 'About', info)