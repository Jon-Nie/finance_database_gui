import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from sidebar import SideBar
from top_bar import TopBar
from pages import Pages

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(150, 100, 1600, 900)
        #self.setWindowFlags(Qt.Window.FramelessWindowHint)

        self.central = QWidget(self)
        self.central.setStyleSheet(
            """
            background-color: #F6F8FB
            """
        )
        self.setCentralWidget(self.central)

        self.layout = QHBoxLayout(self.central)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(10)

        self.sidebar = SideBar()
        self.layout.addWidget(self.sidebar)

        self.content = Content()
        self.layout.addWidget(self.content)

        for button in self.sidebar.buttons:
            button.clicked.connect(self.button_clicked)
        
        self.sidebar.home_button.animateClick()

        self.content.topbar.minimize_button.clicked.connect(self.showMinimized)
        self.content.topbar.maximize_button.clicked.connect(self.maximize_restore)
        self.content.topbar.close_button.clicked.connect(self.close)

    def maximize_restore(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def button_clicked(self):
        sender = self.sender()
        for button in self.button_page_match:
            button.setStyleSheet(
                f"""
                QPushButton {{
                    border: None;
                    color: #A1A1A1;
                    font-family: Lato;
                    font-size: 14px;
                    text-align: left;
                    padding: 10px 0px 10px 15px
                }}
                QPushButton:hover {{
                    border: None;
                    color: #406BD9;
                    background-color: #F6F8FB;
                    font-family: Lato;
                    font-size: 14px;
                    text-align: left;
                    padding: 10px 0px 10px 15px;
                    icon: url(icons/{self.button_icon_match[button]}_blue.svg)
                }}
                """
            )
        self.content.pages.setCurrentWidget(self.button_page_match[sender])
        
        sender.setStyleSheet(
            f"""
            QPushButton {{
                border: none;
                border-left: 4px solid;
                border-color: #406BD9;
                color: #406BD9;
                background-color: #F6F8FB;
                font-family: Lato;
                font-size: 14px;
                text-align: left;
                padding: 10px 0px 10px 15px;
                icon: url(icons/{self.button_icon_match[sender]}_blue.svg)
            }}
            """
        )

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

        self.topbar = TopBar()
        self.layout.addWidget(self.topbar)

        self.pages = Pages()
        self.layout.addWidget(self.pages)

        self.topbar.search_box.returnPressed.connect(self.update_page)
    
    def update_page(self):
        ticker = self.topbar.search_box.text().split("|")[0].strip()
        self.pages.stock_page.update_data(ticker)
        self.pages.setCurrentWidget(self.pages.stock_page)

if __name__ == "__main__":
    app = QApplication()
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())