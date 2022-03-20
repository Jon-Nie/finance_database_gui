import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from stylesheets import app_css, sidebar_button_css
from sidebar import SideBar
from pages import Pages

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(150, 50, 1600, 900)

        self.central = QWidget(self)
        self.central.setStyleSheet(app_css)
        self.setCentralWidget(self.central)

        self.layout = QHBoxLayout(self.central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.sidebar = SideBar()
        for button in self.sidebar.buttons:
            button.clicked.connect(self.sidebar_button_clicked)
        self.sidebar.home_button.animateClick()
        
        self.layout.addWidget(self.sidebar)

        self.content = Content()
        self.layout.addWidget(self.content)

    def sidebar_button_clicked(self):
        sender = self.sender()
        for button in self.button_page_match:
            button.setObjectName("inactive")
            button.setStyleSheet(sidebar_button_css.format(self.button_icon_match[button]))
        self.content.pages.setCurrentWidget(self.button_page_match[sender])
        
        sender.setObjectName("active")
        sender.setStyleSheet(sidebar_button_css.format(self.button_icon_match[sender]))

        self.content.pages.setCurrentWidget(self.button_page_match[sender])

    @property
    def button_page_match(self):
        dct = {
            self.sidebar.home_button : self.content.pages.home_page,
            self.sidebar.equities_button : self.content.pages.equities_page,
            self.sidebar.commodities_button : self.content.pages.commodities_page,
            self.sidebar.economics_button : self.content.pages.economics_page,
            self.sidebar.tracker_button : self.content.pages.tracker_page,
            self.sidebar.backtests_button : self.content.pages.backtests_page
        }
        return dct
    
    @property
    def button_icon_match(self):
        dct = {
            self.sidebar.home_button : "home",
            self.sidebar.equities_button : "equities",
            self.sidebar.commodities_button : "commodities",
            self.sidebar.economics_button : "economics",
            self.sidebar.tracker_button: "tracker",
            self.sidebar.backtests_button: "backtests"
        }
        return dct


class Content(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.topbar = QFrame()
        self.layout.addWidget(self.topbar)

        self.pages = Pages()
        self.layout.addWidget(self.pages)


if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())