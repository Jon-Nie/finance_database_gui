import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from top_bar import *
from sidebar import *
from top_bar import *
from pages.pages import Pages
from stylesheets import app_css, grip_css

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


        self.size_grip_left = QFrame(self)
        self.size_grip_left.setStyleSheet(grip_css)
        self.size_grip_left.setCursor(Qt.SizeHorCursor)
        self.size_grip_left.installEventFilter(self)

        self.size_grip_top = QFrame(self)
        self.size_grip_top.setStyleSheet(grip_css)
        self.size_grip_top.setCursor(Qt.SizeVerCursor)
        self.size_grip_top.installEventFilter(self)

        self.size_grip_right = QFrame(self)
        self.size_grip_right.setStyleSheet(grip_css)
        self.size_grip_right.setCursor(Qt.SizeHorCursor)
        self.size_grip_right.installEventFilter(self)

        self.size_grip_bottom = QFrame(self)
        self.size_grip_bottom.setStyleSheet(grip_css)
        self.size_grip_bottom.setCursor(Qt.SizeVerCursor)
        self.size_grip_bottom.installEventFilter(self)

        self.size_grip_top_left = QSizeGrip(self)
        self.size_grip_top_left.setStyleSheet(grip_css)

        self.size_grip_top_right = QSizeGrip(self)
        self.size_grip_top_right.setStyleSheet(grip_css)

        self.size_grip_bottom_right = QSizeGrip(self)
        self.size_grip_bottom_right.setStyleSheet(grip_css)

        self.size_grip_bottom_left = QSizeGrip(self)
        self.size_grip_bottom_left.setStyleSheet(grip_css)
    
    def paintEvent(self, event):
        width, height = 5, 5

        self.size_grip_left.setGeometry(0, 0, width, self.height())
        self.size_grip_top.setGeometry(0, 0, self.width(), height)
        self.size_grip_right.setGeometry(self.width() - width, 0, width, self.height())
        self.size_grip_bottom.setGeometry(0, self.height() - height, self.width(), height)
        
        self.size_grip_top_left.setGeometry(0, 0, width, height)
        self.size_grip_top_right.setGeometry(self.width() - width, 0, width, height)
        self.size_grip_bottom_right.setGeometry(self.width() - width, self.height() - height, width, height)
        self.size_grip_bottom_left.setGeometry(0, self.height() - height, width, height)
    
    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseMove:
            mouse_position = event.globalPos()
            width = self.geometry().width()
            height = self.geometry().height()
            if object == self.size_grip_left:
                self.setGeometry(mouse_position.x(), self.geometry().y(), self.geometry().x() + width - mouse_position.x(), height)
            if object == self.size_grip_top:
                self.setGeometry(self.geometry().x(), mouse_position.y(), width, self.geometry().y() + height - mouse_position.y())
            if object == self.size_grip_right:
                self.setGeometry(self.geometry().x(), self.geometry().y(), mouse_position.x() - self.geometry().x(), height)
            if object == self.size_grip_bottom:
                self.setGeometry(self.geometry().x(), self.geometry().y(), width, mouse_position.y() - self.geometry().y())
            return True
        return super().eventFilter(object, event)

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