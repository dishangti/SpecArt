import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import welcome

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QtWidgets.QApplication(sys.argv)
welcome_Form = QtWidgets.QWidget()
ui = welcome.Ui_Form()
ui.setupUi(welcome_Form)
welcome_Form.show()
sys.exit(app.exec_())
