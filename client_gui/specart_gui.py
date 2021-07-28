import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import login

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QtWidgets.QApplication(sys.argv)
login_Form = QtWidgets.QWidget()
ui = login.Ui_login_Form()
ui.setupUi(login_Form)
login_Form.show()
sys.exit(app.exec_())
