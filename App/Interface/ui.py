import threading, os, signal, win32con, time, keyboard
from PyQt5 import QtCore, QtWidgets, uic, QtGui
import win32api, win32gui
from PyQt5.QtCore import Qt
import App.command.config as cfg
from App.Interface.popup import choose

if not os.path.isfile(os.path.dirname(__file__) + "settings.ini"):
    cfg.createConfig()
config = cfg.readConfig()

troveHwnd = win32gui.FindWindow(0, "Trove")
whandle = troveHwnd
pid = win32api.GetCurrentProcessId()

def box_coll(x, y, sizex, sizey, posx, posy):
    if posx > x and posx < x + sizex:
        if posy > y and posy < y + sizey:
            return True
    return False

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        self.processes = []
        self.window_handle = whandle
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        uic.loadUi('App/Interface/ui/main.ui', self)
        self.oldPos = None
        self.startPos = None
        self.resizeSize = 10
        self.grabSize = 30
        self.setGeometry(config["pos"][0], config["pos"][1], config["size"][0], config["size"][1])

        self.modal_open = False
        self.stop_event = threading.Event()
        self.worker_thread = None

        self.grabber = self.findChild(QtWidgets.QWidget, 'sidebar')
        self.closeBtn = self.findChild(QtWidgets.QPushButton, 'closeBtn')
        self.closeBtn.released.connect(self.close_ui)
        self.minBtn = self.findChild(QtWidgets.QPushButton, 'minimizeBtn')
        self.minBtn.released.connect(self.minimize)

        # views
        self.class_view = self.findChild(QtWidgets.QWidget, 'ClassView')
        self.other_view = self.findChild(QtWidgets.QWidget, 'OtherView')
        self.class_view.show()
        self.other_view.hide()

        self.class_btn = self.findChild(QtWidgets.QPushButton, 'classChange')
        self.class_btn.released.connect(lambda: self.switch_view(1))
        self.other_btn = self.findChild(QtWidgets.QPushButton, 'otherBtn')
        self.other_btn.released.connect(lambda: self.switch_view(2))

        self.zoom = self.findChild(QtWidgets.QCheckBox, 'Zoom')
        self.hide_player = self.findChild(QtWidgets.QCheckBox, 'hidePlayer')
        self.hide_player.stateChanged.connect(self.visibility)
        self.no_afk = self.findChild(QtWidgets.QCheckBox, 'NoAfk')
        self.no_afk.stateChanged.connect(self.afkbtn)
        self.whisper = self.findChild(QtWidgets.QCheckBox, 'whisper')
        #self.whisper.stateChanged.connect(self.auto_whis)
        self.join = self.findChild(QtWidgets.QCheckBox, 'join')
        #self.join.stateChanged.connect(self.auto_join)
        self.hit = self.findChild(QtWidgets.QCheckBox, 'hit')
        self.hit.stateChanged.connect(self.auto_hit)

        self.class_btn_1 = self.findChild(QtWidgets.QPushButton, 'class_btn_1')
        self.class_btn_1.released.connect(lambda: self.switch_class(self.class_btn_1, whandle))
        self.class_btn_2 = self.findChild(QtWidgets.QPushButton, 'class_btn_2')
        self.class_btn_2.released.connect(lambda: self.switch_class(self.class_btn_2, whandle))
        self.class_btn_3 = self.findChild(QtWidgets.QPushButton, 'class_btn_3')
        self.class_btn_3.released.connect(lambda: self.switch_class(self.class_btn_3, whandle))

        self.open = self.findChild(QtWidgets.QPushButton, 'open')
        self.open.released.connect(self.open_dialog)
        self.selected_classes = []
    
        self.load()
        self.show()

    def load(self):
        config_data = cfg.readConfig()
        selected_classes = [class_name.strip("[]' ") for class_name in config_data["selected_classes"]]
        selected_images = [f"App/Interface/imgs/{class_name.strip('[]' ).replace(' ', '')}.png" for class_name in selected_classes]
        self.update_class_buttons(selected_classes, selected_images)
    def open_dialog(self):
        if self.modal_open:
            return
        
        self.modal_open = True
        self.dialog = choose(self)
        self.dialog.show()
    def update_class_buttons(self, class_texts, image_paths):
        buttons = [self.class_btn_1, self.class_btn_2, self.class_btn_3]

        for button, text, path in zip(buttons, class_texts, image_paths):
            button.setText(f" {text}")
            button.setIcon(QtGui.QIcon(path))
    def save_config(self, selected_classes):
        cfg.writeConfig(selected_classes=selected_classes)


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


    def switch_view(self, arg):
        if arg == 1:
            self.class_view.show()
            self.other_view.hide()
        else:
            self.class_view.hide()
            self.other_view.show()
    def minimize(self):
        if self.isMinimized():
            self.showNormal()
        else:
            self.showMinimized()
    def close_ui(self):
        cfg.writeConfig(f"{self.size().width()},{self.size().height()}", f"{self.pos().x()},{self.pos().y()}")
        os.kill(pid, signal.SIGTERM)

    def action(self, first_click_x, first_click_y, key_press, second_click_coords, window_handle):
        screen_resolution = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        if screen_resolution == (1920, 1080):
            second_click_x, second_click_y = second_click_coords['1920x1080']
        else:
            print("Invalid screen resolution")
            return

        win32gui.SetActiveWindow(whandle)

        win32api.SetCursorPos((first_click_x, first_click_y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, first_click_x, first_click_y, 0, 0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, first_click_x, first_click_y, 0, 0)
        keyboard.press_and_release('j')
        time.sleep(0.5)

        win32api.SetCursorPos((second_click_x, second_click_y))
        win32api.mouse_event( win32con.MOUSEEVENTF_LEFTDOWN, second_click_x, second_click_y, 0, 0)
        win32api.mouse_event( win32con.MOUSEEVENTF_LEFTUP, second_click_x, second_click_y, 0, 0)
        time.sleep(1)
    def switch_class(self, button, whandle):
        class_text = button.text().strip()
        match class_text:
            case 'Solarion':
                self.action(1280, 540, 'j', {
                    '1920x1080': (0, 0)
                }, whandle)
                print(f'class ok {class_text}')
            case 'Ice Sage':
                print(f'class ok {class_text}')
            case 'Bard':
                print(f'class ok {class_text}')
            case 'Shadow Hunter':
                print(f'class ok {class_text}')
            case 'Dracolyte':
                print(f'class ok {class_text}')
            case 'Boomeranger':
                print(f'class ok {class_text}')

    def visibility(self):
        if self.hidePlayer.isChecked():
            message = "Hide Player"
            wParam = [0x2F, 0x68, 0x69, 0x64, 0x65, 0x70, 0x6C, 0x61, 0x79, 0x65, 0x72]
        else:
            message = "Show Player"
            wParam = [0x2F, 0x73, 0x68, 0x6F, 0x77, 0x70, 0x6C, 0x61, 0x79, 0x65, 0x72]

        try:
            for i in range(len(wParam)):
                win32api.PostMessage(whandle, win32con.WM_CHAR, wParam[i], 0)
            win32api.PostMessage(whandle, win32con.WM_KEYDOWN, 0x0D, 0x1C0001)
            win32api.PostMessage(whandle, win32con.WM_KEYUP, 0x0D, 0x1C0001)
            print(message)
        except:
            exit(0)

    def afkbtn(self, state):
        if state == QtCore.Qt.Checked:
            self.stop_event.clear()
            self.worker_thread = threading.Thread(target=self.anti_afk, args=(self.stop_event,))
            self.worker_thread.start()
        else:
            self.stop_event.set()
    def anti_afk(self, stop_event):
        while not stop_event.is_set():
            win32api.PostMessage(troveHwnd, win32con.WM_CHAR)
            win32api.PostMessage(troveHwnd, win32con.WM_KEYDOWN,  0x20, 0x390001)
            win32api.PostMessage(troveHwnd, win32con.WM_KEYUP,  0x20, 0x390001)
            time.sleep(200)

    def auto_hit(self, state):
        if state == QtCore.Qt.Checked:
            self.stop_event.clear()
            self.worker_thread = threading.Thread(target=self.a_hit, args=(self.stop_event,))
            self.worker_thread.start()
        else:
            self.stop_event.set()
    def a_hit(self, stop_event):
        if self.hit.isChecked():
            print("Activé")  
            while not stop_event.is_set():
                win32gui.SendMessage(troveHwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
            else:
                print("Désactivé")
                win32gui.SendMessage(troveHwnd, win32con.WM_LBUTTONUP)