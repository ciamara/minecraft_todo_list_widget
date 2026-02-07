import os
os.environ["QT_PA_PLATFORM"] = "windows:dpiawareness=1"
#import ctypes
from pynput import keyboard
#from PIL import Image
import pandas as pd

import sys
from PyQt6.QtWidgets import QApplication, QLabel, QWidget
from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtGui import QFont

from todo_overlay import TodoOverlay



def update_list():

    todos = ''
    overlay.data_received.emit(todos)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    global overlay
    overlay = TodoOverlay()

    overlay.show()

    overlay.raise_()
    overlay.activateWindow()


    #listener = keyboard.GlobalHotKeys({'<f9>': update_list})
    #listener.start() 

    sys.exit(app.exec())