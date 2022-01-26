import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from welcome_set import mainWin

QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
app = QtWidgets.QApplication(sys.argv)
ui = mainWin()
ui.show()
sys.exit(app.exec_())
