import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from top_bar import *
from sidebar import *
from top_bar import *
from pages.pages import Pages
from stylesheets import (
    app_css,
    grip_css,
    button_frame_css,
    minimize_css,
    maximize_css,
    close_css
)

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(175, 50, 1600, 900)
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

        for button in self.button_page_match:
            button.clicked.connect(self.update_page_style)
    
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
    
    @property
    def button_page_match(self):
        dct = {
            self.sidebar.button_frame.home_button: self.content.pages.home_page,
            self.sidebar.button_frame.equities_button: self.content.pages.equities_page,
            self.sidebar.button_frame.commodities_button: self.content.pages.commodities_page,
            self.sidebar.button_frame.economics_button: self.content.pages.economics_page,
            self.sidebar.button_frame.tracker_button: self.content.pages.tracker_page,
            self.sidebar.button_frame.backtests_button: self.content.pages.backtests_page,

            self.content.pages.home_page.equities_box.button: self.content.pages.equities_page,
            self.content.pages.home_page.commodities_box.button: self.content.pages.commodities_page,
            self.content.pages.home_page.economics_box.button: self.content.pages.economics_page,
            self.content.pages.home_page.tracker_box.button: self.content.pages.tracker_page,
            self.content.pages.home_page.backtests_box.button: self.content.pages.backtests_page,
            self.content.pages.equities_page.stocks_box.button: self.content.pages.stocks_page,
            self.content.pages.equities_page.industries_box.button: self.content.pages.industries_page,
            self.content.pages.equities_page.institutionals_box.button: self.content.pages.institutionals_page,
            self.content.pages.equities_page.analysts_box.button: self.content.pages.analysts_page,
            self.content.pages.equities_page.factors_box.button: self.content.pages.factors_page,
        }
        return dct
    
    @property
    def page_sidebar_match(self):
        dct = {
            self.content.pages.home_page: self.sidebar.button_frame.home_button,
            self.content.pages.equities_page: self.sidebar.button_frame.equities_button,
            self.content.pages.commodities_page: self.sidebar.button_frame.commodities_button,
            self.content.pages.economics_page: self.sidebar.button_frame.economics_button,
            self.content.pages.tracker_page: self.sidebar.button_frame.tracker_button,
            self.content.pages.backtests_page: self.sidebar.button_frame.backtests_button,

            self.content.pages.equities_page: self.sidebar.button_frame.equities_button,
            self.content.pages.commodities_page: self.sidebar.button_frame.commodities_button,
            self.content.pages.economics_page: self.sidebar.button_frame.economics_button,
            self.content.pages.tracker_page: self.sidebar.button_frame.tracker_button,
            self.content.pages.backtests_page: self.sidebar.button_frame.backtests_button,
            self.content.pages.stocks_page: self.sidebar.button_frame.equities_button,
            self.content.pages.industries_page: self.sidebar.button_frame.equities_button,
            self.content.pages.institutionals_page: self.sidebar.button_frame.equities_button,
            self.content.pages.analysts_page: self.sidebar.button_frame.equities_button,
            self.content.pages.factors_page: self.sidebar.button_frame.equities_button,
        }
        return dct
    
    def update_page_style(self):
        page = self.button_page_match[self.sender()]
        self.content.pages.setCurrentWidget(page)
        self.content.setStyleSheet(page.background())
        if page == self.content.pages.home_page:
            self.sidebar.button_frame.setObjectName("blue")
            self.content.topbar.minimize_button.setObjectName("blue")
            self.content.topbar.maximize_button.setObjectName("blue")
            self.content.topbar.close_button.setObjectName("blue")
        else:
            self.sidebar.button_frame.setObjectName("white")
            self.content.topbar.minimize_button.setObjectName("white")
            self.content.topbar.maximize_button.setObjectName("white")
            self.content.topbar.close_button.setObjectName("white")
        self.sidebar.button_frame.setStyleSheet(button_frame_css)
        self.content.topbar.minimize_button.setStyleSheet(minimize_css)
        self.content.topbar.maximize_button.setStyleSheet(maximize_css)
        self.content.topbar.close_button.setStyleSheet(close_css)

        self.sidebar.button_frame.change_stylesheet_from_outside(self.page_sidebar_match[self.button_page_match[self.sender()]])


class Content(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.topbar = TopBar()
        self.layout.addWidget(self.topbar)

        self.pages = Pages()
        self.layout.addWidget(self.pages)
    
if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())