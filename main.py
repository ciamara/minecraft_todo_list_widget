import sys
from PyQt6.QtWidgets import QApplication

from todo_overlay import TodoOverlay
    

def entry_handler():
    overlay.load()

def exit_handler():
    overlay.save()


if __name__ == "__main__":

    global app
    app = QApplication(sys.argv)

    global overlay
    overlay = TodoOverlay()

    entry_handler()

    overlay.show()

    overlay.raise_()
    overlay.activateWindow()

    app.aboutToQuit.connect(exit_handler)

    sys.exit(app.exec())