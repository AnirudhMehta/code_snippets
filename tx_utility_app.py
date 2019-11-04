import sys
from PyQt5 import  QtGui, QtWidgets
from ui_modules import Ui_MainWindow_with_Funcs

def main():
    app = QtWidgets.QApplication( sys.argv )
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow_with_Funcs()
    ui.setupUi( MainWindow )
    MainWindow.show()
    sys.exit( app.exec_() )

main()