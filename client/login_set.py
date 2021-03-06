from PyQt5.QtWidgets import QMainWindow, QMessageBox
from login import Ui_MainWindow
import mainwin_set
 
class mainWin(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(mainWin, self).__init__()

        self.setupUi(self)

        self.lineEdit_init()
        self.pushButton_init()
        self.lineEdit.setFocus()

        self.setFixedSize(self.width(), self.height())

    def lineEdit_init(self):
        '''
        将输入栏文本变化与self.check_input函数绑定
        '''
        self.lineEdit.textChanged.connect(self.check_input)
        self.lineEdit_2.textChanged.connect(self.check_input)
        self.lineEdit.returnPressed.connect(self.waitForServer)
        self.lineEdit_2.returnPressed.connect(self.waitForServer)

    def check_input(self):
        '''
        两输入栏均有文本时让“登录”按钮可用
        '''
        if self.lineEdit.text() and self.lineEdit_2.text():
            self.pushButton.setEnabled(True)
        else:
            self.pushButton.setEnabled(False)
    
    def pushButton_init(self):
        '''
        初始化“登录”按钮为不可用，将按钮被点击与waitForServer函数绑定
        '''
        self.pushButton.setEnabled(False)
        self.pushButton.clicked.connect(self.waitForServer)

    def waitForServer(self):
        '''
        点击“登录”按钮后改变按钮状态，并创建mainwin类与服务器沟通
        '''
        if not self.pushButton.isEnabled(): return
        self.username = self.lineEdit.text()
        self.host = self.lineEdit_2.text()

        self.window = mainwin_set.mainWin()
        try:
            self.pushButton.setText('Loging in...')
            self.pushButton.setEnabled(False)
            self.window.com.connect(self.username, self.host)
        except Exception:
            self.window.com.notice("Connection failed! Check your network and address please.")
            self.pushButton.setText('Login')
            self.pushButton.setEnabled(True)
        else:
            self.window.com.notice('Success! Wait for the game beginning...')
            self.window.show()
            self.close()

