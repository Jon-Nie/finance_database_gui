import sys
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from stylesheets import (
    app_css,
    sidebar_button_css,
    sidebar_button_sub_css,
    sidebar_button_super_css
)
from sidebar import *
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
        if isinstance(sender, SidebarButtonSuper):
            if self.super_sub_match[sender][0].height() == 0:
                for sub_button in self.super_sub_match[sender]:
                    self.sidebar.animation(sub_button, sub_button.height(), 35)
        elif not isinstance(sender, SidebarButtonSub):
            for super_button in self.super_sub_match:
                for sub_button in self.super_sub_match[super_button]:
                    self.sidebar.animation(sub_button, sub_button.height(), 0)
        
        for button in self.sidebar.buttons:
            button.setObjectName("inactive")
            if isinstance(button, SidebarButton):
                button.setStyleSheet(sidebar_button_css.format(self.button_icon_match[button]))
            elif isinstance(button, SidebarButtonSuper):
                button.setStyleSheet(sidebar_button_super_css.format(self.button_icon_match[button]))
            elif isinstance(button, SidebarButtonSub):
                button.setStyleSheet(sidebar_button_sub_css)
        
        sender.setObjectName("active")
        if isinstance(sender, SidebarButton):
            sender.setStyleSheet(sidebar_button_css.format(self.button_icon_match[sender]))
        elif isinstance(sender, SidebarButtonSuper):
            sender.setStyleSheet(sidebar_button_super_css.format(self.button_icon_match[sender]))
        elif isinstance(sender, SidebarButtonSub):
            sender.setStyleSheet(sidebar_button_sub_css)
        
        if not isinstance(sender, SidebarButtonSuper):
            self.content.pages.setCurrentWidget(self.button_page_match[sender])

    @property
    def button_page_match(self):
        dct = {
            self.sidebar.home_button : self.content.pages.home_page,
            self.sidebar.stocks_button : self.content.pages.stocks_page,
            self.sidebar.industries_button : self.content.pages.industries_page,
            self.sidebar.analysts_button : self.content.pages.analysts_page,
            self.sidebar.institutionals_button : self.content.pages.institutionals_page,
            self.sidebar.factors_button : self.content.pages.factors_page,
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

    @property
    def super_sub_match(self):
        dct = {
            self.sidebar.equities_button: [
                self.sidebar.stocks_button,
                self.sidebar.industries_button,
                self.sidebar.analysts_button,
                self.sidebar.institutionals_button,
                self.sidebar.factors_button
            ]
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