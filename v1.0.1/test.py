import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication, QLabel, QMenu, QTextEdit
from PyQt5.QtWidgets import QTextBrowser, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QHBoxLayout, QDesktopWidget
from PyQt5.QtGui import QTextDocument
import mistune


class PetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.image_path = "Default.png"
        self.init_ui()
        self.move_to_corner()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.keep_window_alive)
        self.timer.start(1000)

        self.m_drag = False
        self.m_DragPosition = None

        self.settings_window = SettingsWindow()
        self.chat_window = ChatWindow()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(Qt.ArrowCursor)

    def init_ui(self):
        pixmap = QPixmap(self.image_path)
        if pixmap.isNull():
            print(f"Error: Failed to load image from path: {self.image_path}")
            return

        self.setFixedSize(pixmap.width(), pixmap.height())

        self.image_label = QLabel(self)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)
        self.image_label.setGeometry(0, 0, pixmap.width(), pixmap.height())

        self.image_label.setContextMenuPolicy(Qt.CustomContextMenu)
        self.image_label.customContextMenuRequested.connect(self.show_menu)

    def move_to_corner(self):
        screen_geometry = QDesktopWidget().availableGeometry()
        screen_right_bottom_corner = screen_geometry.bottomRight()
        self.move(screen_right_bottom_corner - self.rect().bottomRight())

    def show_menu(self, pos):
        menu = QMenu(self)
        menu.addAction("Ask LLM", self.chat)
        menu.addAction("Setting", self.setting)
        menu.addAction("Exit", self.close)
        menu.exec_(self.mapToGlobal(pos))

    def keep_window_alive(self):
        self.setVisible(True)

    def chat(self):
        self.chat_window.show()

    def setting(self):
        self.settings_window.show()

    def close(self):
        exit(0)

    def focusOutEvent(self, event):
        super().focusOutEvent(event)

class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # window settings
        self.setWindowTitle('Asking LLM')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        # chat history display
        self.text_browser = QTextBrowser(self)

        # message input
        self.line_edit = QLineEdit(self)
        self.line_edit.returnPressed.connect(self.send_message)

        # button
        self.send_button = QPushButton('Send', self)
        self.send_button.clicked.connect(self.send_message)

        other_button = QPushButton('Other', self)

        # layout settings
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_button)
        button_layout.addWidget(other_button)

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.text_browser)
        main_layout.addWidget(self.line_edit)
        main_layout.addLayout(button_layout)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)

        self.setCentralWidget(main_widget)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()
            self.setCursor(Qt.OpenHandCursor)

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.m_drag:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_drag = False
        self.setCursor(Qt.ArrowCursor)

    def set_markdown(self, markdown_string):
        renderer = mistune.Renderer(escape=True, hard_wrap=True)
        markdown = mistune.Markdown(renderer=renderer)
        html = markdown(markdown_string)
        self.text_browser.append(html)

    def send_message(self):
        message = self.line_edit.text()
        self.line_edit.clear()
        if message:
            self.text_browser.append(message)

class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Setting')

    def keep_window_alive(self):
        self.setVisible(True)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PetWindow()
    window.show()
    sys.exit(app.exec_())
