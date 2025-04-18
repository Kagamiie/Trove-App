import os, time, threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox
import keyboard
from pynput.mouse import Listener as MouseListener
import win32gui, win32con, win32api
from config import create_config, write_config, read_config, delete_profil

def find_trove_window(): return win32gui.FindWindow(0, "Trove")
def ensure_config_exists():
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "settings.json")):
        create_config()

class UserInterface:
    def __init__(self, root):
        self.root, self.trove_hwnd = root, find_trove_window()
        self.root.title("Trove Helper")
        self.root.geometry("670x400")
        self.root.resizable(False, False)

        self.current_profil_events, self.recording_in_progress = [], False
        self.run_profil_checkbox_var = tk.BooleanVar()

        self._build_ui()
        self._update_profil_menu()

    def _log(self, msg):
        self.console.config(state='normal')
        self.console.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.console.config(state='disabled')
        self.console.yview(tk.END)

    def _start_thread(self, func): threading.Thread(target=func, daemon=True).start()
    def _update_profil_menu(self): self.profil_dropdown['values'] = list(read_config().get("profil", {}).keys())

    def save(self):
        name = self.profil_name.get()
        if not name: return self._log("Enter a profil name.")
        try:
            interval = float(self.float_entry.get())
            write_config(profil={name: self.current_profil_events}, interval=interval)
            self._log(f"Profil '{name}' saved.")
            self._update_profil_menu()
        except ValueError:
            self._log("Invalid interval format.")

    def load(self, _=None):
        name = self.profil_dropdown.get()
        config = read_config()
        profil = config.get("profil", {}).get(name)
        if not profil: return self._log("Invalid profil.")
        self.current_profil_events = profil
        self.float_entry.delete(0, tk.END)
        self.float_entry.insert(0, str(config.get("interval", 1.5)))
        self._update_live_record()
        self._log(f"Profil '{name}' loaded.")

    def delete(self):
        name = self.profil_dropdown.get()
        if not name: return self._log("Select a profil to delete.")
        if messagebox.askyesno("Confirm", f"Delete profil '{name}'?"):
            delete_profil(name)
            self._update_profil_menu()
            self._log(f"Profil '{name}' deleted.")

    def _build_ui(self):
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Profil Name:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        self.profil_name = ttk.Entry(main_frame, width=25)
        self.profil_name.grid(row=0, column=1, sticky='w')

        ttk.Label(main_frame, text="Interval (s):").grid(row=1, column=0, sticky='e', padx=5, pady=5)
        self.float_entry = ttk.Entry(main_frame, width=10)
        self.float_entry.grid(row=1, column=1, sticky='w')
        self.float_entry.insert(0, "1.5")

        ttk.Label(main_frame, text="Select Profil:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
        self.profil_var = tk.StringVar()
        self.profil_dropdown = ttk.Combobox(main_frame, textvariable=self.profil_var, state='readonly', width=22)
        self.profil_dropdown.grid(row=2, column=1, sticky='w')
        self.profil_dropdown.set("Select a profil")
        self.profil_dropdown.bind("<<ComboboxSelected>>", self.load)

        self.live_record_entry = ttk.Entry(main_frame, width=60, state='readonly')
        self.live_record_entry.grid(row=3, column=0, columnspan=3, pady=10)

        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, columnspan=3, pady=5)
        ttk.Button(action_frame, text="Record", command=self.toggle_recording).grid(row=0, column=0, padx=5)
        ttk.Button(action_frame, text="Save", command=self.save).grid(row=0, column=1, padx=5)
        ttk.Button(action_frame, text="Do Once", command=lambda: self._start_thread(self._macro_once)).grid(row=0, column=2, padx=5)
        ttk.Button(action_frame, text="Delete", command=self.delete).grid(row=0, column=3, padx=5)

        toggles = ttk.Frame(main_frame)
        toggles.grid(row=5, column=0, columnspan=3, pady=10)
        self.hide_var = tk.BooleanVar()
        self.afk_var = tk.BooleanVar()
        self.auto_var = tk.BooleanVar()
        ttk.Checkbutton(toggles, text="Hide Player", variable=self.hide_var, command=self.toggle_visibility).grid(row=0, column=0, padx=5)
        ttk.Checkbutton(toggles, text="Anti AFK", variable=self.afk_var, command=lambda: self._start_thread(self._anti_afk)).grid(row=0, column=1, padx=5)
        ttk.Checkbutton(toggles, text="Auto Hit", variable=self.auto_var, command=lambda: self._start_thread(self._auto_hit)).grid(row=0, column=2, padx=5)
        ttk.Checkbutton(toggles, text="Loop Profil", variable=self.run_profil_checkbox_var, command=lambda: self._start_thread(self._macro_loop)).grid(row=0, column=3, padx=5)

        self.console = tk.Text(main_frame, height=10, width=80, state='disabled', bg="#f0f0f0")
        self.console.grid(row=6, column=0, columnspan=3, pady=10)

    def _update_live_record(self):
        self.live_record_entry.config(state='normal')
        self.live_record_entry.delete(0, tk.END)
        self.live_record_entry.insert(0, ", ".join(self.current_profil_events))
        self.live_record_entry.config(state='readonly')

    def toggle_recording(self):
        if self.recording_in_progress:
            self.recording_in_progress = False
            keyboard.unhook_all()
            self.mouse_listener.stop()
            self.mouse_listener.join()
            if self.current_profil_events: self.current_profil_events.pop()
        else:
            self.recording_in_progress = True
            self.current_profil_events = []
            keyboard.hook(self._on_key)
            self.mouse_listener = MouseListener(on_click=self._on_mouse)
            self.mouse_listener.start()
        self._update_live_record()

    def toggle_visibility(self):
        base = [0x2F]
        base += ([0x68, 0x69, 0x64, 0x65] if self.hide_var.get() else [0x73, 0x68, 0x6F, 0x77])
        base += [0x70, 0x6C, 0x61, 0x79, 0x65, 0x72]
        for c in base: win32api.PostMessage(self.trove_hwnd, win32con.WM_CHAR, c, 0)
        win32api.PostMessage(self.trove_hwnd, win32con.WM_KEYDOWN, 0x0D, 0x1C0001)
        win32api.PostMessage(self.trove_hwnd, win32con.WM_KEYUP, 0x0D, 0x1C0001)

    def _on_key(self, e):
        if self.recording_in_progress and e.event_type == keyboard.KEY_DOWN:
            self.current_profil_events.append(e.name)
            self._update_live_record()

    def _on_mouse(self, x, y, button, pressed):
        if self.recording_in_progress and pressed:
            self.current_profil_events.append(button.name)
            self._update_live_record()

    def _macro_once(self):
        try:
            keys = self.live_record_entry.get().strip().split(", ")
            interval = float(self.float_entry.get())
            for key in keys:
                if not key.isalnum(): continue
                wParam = ord(key.upper())
                param = win32api.MapVirtualKey(wParam, 0) << 16 | 1
                win32api.PostMessage(self.trove_hwnd, win32con.WM_KEYDOWN, wParam, param)
                time.sleep(interval)
                win32api.PostMessage(self.trove_hwnd, win32con.WM_KEYUP, wParam, 0xC0 << 24 | param)
                time.sleep(interval)
            self._log("Profil executed once.")
        except Exception as e:
            self._log(f"Execution error: {e}")

    def _macro_loop(self):
        while self.run_profil_checkbox_var.get():
            self._macro_once()

    def _anti_afk(self):
        while self.afk_var.get():
            win32api.PostMessage(self.trove_hwnd, win32con.WM_KEYDOWN, 0x20, 0x390001)
            time.sleep(0.2)
            win32api.PostMessage(self.trove_hwnd, win32con.WM_KEYUP, 0x20, 0x390001)
            time.sleep(200)

    def _auto_hit(self):
        while self.auto_var.get():
            win32gui.SendMessage(self.trove_hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON)
        win32gui.SendMessage(self.trove_hwnd, win32con.WM_LBUTTONUP, 0, 0)

if __name__ == "__main__":
    ensure_config_exists()
    root = tk.Tk()
    UserInterface(root)
    root.mainloop()
