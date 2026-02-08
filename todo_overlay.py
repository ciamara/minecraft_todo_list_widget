from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QTextEdit, QPushButton, QApplication
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer, pyqtSignal

class TodoOverlay(QWidget):

    data_received = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        font_path = "Minecraft.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(font_family, 11)

        self.setWindowFlags(
            Qt.WindowType.Window |
            Qt.WindowType.FramelessWindowHint | 
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.CustomizeWindowHint |
            Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_NoSystemBackground)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # hide timer
        #self.display_timer = QTimer(self)
        #self.display_timer.setSingleShot(True)
        #self.display_timer.timeout.connect(self.hide)

        self.background_label = QLabel("", self)
        self.background_label.setStyleSheet("""
            QLabel {
                border-image: url("book_page.png") 0 0 0 0 stretch stretch;
                border-radius: 8px;
            }
        """)
        
        label_layout = QVBoxLayout(self.background_label)
        label_layout.setContentsMargins(20, 30, 20,30)

        self.close_button = QPushButton("×", self.background_label)
        self.close_button.setFixedSize(24, 24)
        self.close_button.move(160, 5) 
        
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: #2c2c2c;
                font-size: 18px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                color: #aa0000;
            }
        """)

        self.close_button.clicked.connect(lambda: QApplication.instance().quit())

        self.text_editor = QTextEdit()
        self.text_editor.setFont(custom_font)
        self.text_editor.setText("")
        
        self.text_editor.setStyleSheet("""
            QTextEdit {
                background: transparent;
                border: none;
                color: #2c2c2c;
            }
        """)

        label_layout.addWidget(self.text_editor)
        main_layout.addWidget(self.background_label)

        self.data_received.connect(self.update_todos)
        
        self.setGeometry(1340, 500, 190, 240)     # x, y, w, h

    def update_todos(self, todos):
        self.text_editor.setPlainText(todos)
        self.show()
        #self.display_timer.start(6000)

    def load(self):
        with open("save.txt", "r", encoding="utf-8") as f:
            data = f.read()
        self.text_editor.setPlainText(data)
    
    def save(self):
        data = self.text_editor.toPlainText()
        with open("save.txt", "w", encoding="utf-8") as f:
            f.write(data)
