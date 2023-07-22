from PyQt5 import QtCore, QtWidgets, uic
from PyQt5.QtCore import Qt

class choose(QtWidgets.QMainWindow):
    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        uic.loadUi('App/Interface/ui/popup.ui', self)
        self.oldPos = None
        self.startPos = None
        self.resizeSize = 10
        self.grabSize = 30
        
        self.save_btn = self.findChild(QtWidgets.QPushButton, 'Savebtn')
        self.save_btn.released.connect(self.save_selection)

        self.class_btn_1 = self.findChild(QtWidgets.QPushButton, 'Solarion')
        self.class_btn_1.released.connect(lambda: self.select_button(self.Solarion))
        
        self.class_btn_2 = self.findChild(QtWidgets.QPushButton, 'IceSage')   
        self.class_btn_2.released.connect(lambda: self.select_button(self.IceSage))

        self.class_btn_3 = self.findChild(QtWidgets.QPushButton, 'ShadowHunter')
        self.class_btn_3.released.connect(lambda: self.select_button(self.ShadowHunter))

        self.class_btn_4 = self.findChild(QtWidgets.QPushButton, 'Bard')
        self.class_btn_4.released.connect(lambda: self.select_button(self.Bard))

        self.class_btn_5 = self.findChild(QtWidgets.QPushButton, 'Boomeranger')
        self.class_btn_5.released.connect(lambda: self.select_button(self.Boomeranger))

        self.class_btn_6 = self.findChild(QtWidgets.QPushButton, 'Dracolyte')
        self.class_btn_6.released.connect(lambda: self.select_button(self.Dracolyte))

        self.close_btn = self.findChild(QtWidgets.QPushButton, 'closeBtn')
        self.close_btn.released.connect(self.Close)
        self.min_btn = self.findChild(QtWidgets.QPushButton, 'minimizeBtn')
        self.min_btn.released.connect(self.minimize)

        self.grabber = self.findChild(QtWidgets.QWidget, 'sidebar')
        self.selected_classes = []  

    def select_button(self, button):
        if button in self.selected_classes:
            self.selected_classes.remove(button)
            button.setStyleSheet("border: 1px solid rgba(255, 255, 255, 0.096);color:white;")
        elif len(self.selected_classes) < 3:
                self.selected_classes.append(button)
                button.setStyleSheet("background-color: rgba(255,255,255,8); color:white;border: 1px solid rgba(255, 255, 255, 0.096);")
    def save_selection(self):
        selected_classes_text = [button.text() for button in self.selected_classes]
        self.main_window.save_config(selected_classes_text)
        print(selected_classes_text) 

        selected_classes_images = [f'App/Interface/imgs/{button.objectName()}.webp' for button in self.selected_classes]
        self.main_window.update_class_buttons(selected_classes_text, selected_classes_images)
        print(selected_classes_images)

        self.Close()


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = event.globalPos()
    def mouseMoveEvent(self, event):
        if self.oldPos:
            delta = event.globalPos() - self.oldPos
            self.move(self.pos() + delta)
            self.oldPos = event.globalPos()
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.oldPos = None


    def minimize(self):
        if self.isMinimized():
            self.showNormal()
        else:
            self.showMinimized()
    def Close(self):
        self.main_window.modal_open = False
        self.close()