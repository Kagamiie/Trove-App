import win32api, keyboard

keyboard.on_press(lambda _: print({"x": win32api.GetCursorPos()[0], "y": win32api.GetCursorPos()[1]}))
keyboard.wait()