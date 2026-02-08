from PyQt6.QtWidgets import QLabel, QWidget, QVBoxLayout, QTextEdit, QPushButton, QApplication
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QPoint

class TodoOverlay(QWidget):

    def __init__(self):
        super().__init__()

        self._dragging = False
        self._resizing = False
        self._drag_pos = QPoint()
        self.resize_margin = 10

        font_path = "Minecraft.ttf"
        font_id = QFontDatabase.addApplicationFont(font_path)
        self.font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        custom_font = QFont(self.font_family, int(self.width()/50))

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

        self.setMouseTracking(True)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.background_label = QLabel("", self)
        self.background_label.setStyleSheet("""
            QLabel {
                border-image: url("book_page.png") 0 0 0 0 stretch stretch;
                border-radius: 8px;
            }
        """)
        
        label_layout = QVBoxLayout(self.background_label)
        label_layout.setContentsMargins(int(self.width()/25), int(self.width()/25), int(self.width()/25),int(self.width()/25))

        self.close_button = QPushButton("×", self.background_label)
        self.close_button.setFixedSize(24, 24)
        self.close_button.move(150, 4) 
        self.close_button.setContentsMargins(0, 0, 10, 0)
        
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

        
        self.setGeometry(1340, 500, 190, 240)     # x, y, w, h


    def load(self):
        with open("save.txt", "r", encoding="utf-8") as f:
            data = f.read()
        self.text_editor.setPlainText(data)
    
    def save(self):
        data = self.text_editor.toPlainText()
        with open("save.txt", "w", encoding="utf-8") as f:
            f.write(data)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            rect = self.rect()
            if event.pos().x() > rect.width() - self.resize_margin and \
               event.pos().y() > rect.height() - self.resize_margin:
                self._resizing = True
            else:
                self._dragging = True
                self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        rect = self.rect()
        pos = event.pos()

        if pos.x() > rect.width() - self.resize_margin and pos.y() > rect.height() - self.resize_margin:
            self.setCursor(Qt.CursorShape.SizeFDiagCursor)
        else:
            self.setCursor(Qt.CursorShape.ArrowCursor)

        if self._resizing:
            new_width = max(100, pos.x())
            new_height = max(100, pos.y())
            self.resize(new_width, new_height)
        elif self._dragging:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
        
        event.accept()

    def mouseReleaseEvent(self, event):
        self._dragging = False
        self._resizing = False
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def resizeEvent(self, event):
        self.close_button.move(self.width() - 40, 5)
        self.text_editor.move(int(self.width()/10), int(self.height()/9))

        dynamic_size = max(8, int(self.width() / 15)) 
        new_font = QFont(self.font_family, dynamic_size)
        self.text_editor.setFont(new_font)
        super().resizeEvent(event)
