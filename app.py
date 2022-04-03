import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from top_bar import *
from sidebar import *
from top_bar import *
from pages.pages import Pages
from stylesheets import app_css

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(150, 50, 1650, 950)
        self.setWindowFlags(Qt.Window.FramelessWindowHint)
        
        self.central = QWidget(self)
        self.central.setStyleSheet(app_css)
        self.setCentralWidget(self.central)

        self.layout = QHBoxLayout(self.central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.sidebar = SideBar()

        self.layout.addWidget(self.sidebar)

        self.content = Content()
        self.layout.addWidget(self.content)

        self.content.topbar.minimize_button.clicked.connect(self.showMinimized)
        self.content.topbar.maximize_button.clicked.connect(self.maximize_restore)
        self.content.topbar.close_button.clicked.connect(self.close)

        self.content.topbar.mouseMoveEvent = self.moveWindow

    def moveWindow(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.drag_pos)
            self.drag_pos = event.globalPos()
            event.accept()

    def mousePressEvent(self, event):
        self.drag_pos = event.globalPos()

    def maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

class Content(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.topbar = TopBar(self)
        self.layout.addWidget(self.topbar)

        self.pages = Pages()
        self.layout.addWidget(self.pages)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())