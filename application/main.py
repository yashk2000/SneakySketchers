import sys
from gui.model import model
from PyQt5 import QtWidgets
import argparse

def main():
    app = QtWidgets.QApplication(sys.argv)
    parser = argparse.ArgumentParser()
    opt = parser
    inpaint_gui = model(opt)
    inpaint_gui.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
    