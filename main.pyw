from PyQt5.QtWidgets import QApplication
from App import Ui
import sys

def main():
    app = QApplication(sys.argv)
    window = Ui()
    app.exec_()

if __name__ == "__main__":
    main()