import sys
from gui.ui_model import ui_model
from PyQt5 import QtWidgets


if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    my_gui = ui_model()
    my_gui.show()
    sys.exit(app.exec_())
