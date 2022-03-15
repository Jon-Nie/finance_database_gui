from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from stylesheets import (
    sidebar_css,
    sidebar_button_css
)

class SideBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(200)
        self.setStyleSheet(sidebar_css)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.placeholder = QFrame()
        self.placeholder.setFixedHeight(100)
        self.layout.addWidget(self.placeholder)

        self.home_button = SidebarButton(f"Home", "home")
        self.equities_button = SidebarButton(f"Equities", "equities")
        self.commodities_button = SidebarButton(f"Commodities", "commodities")
        self.economics_button = SidebarButton(f"Economic Data", "economics")
        self.tracker_button = SidebarButton(f"Portfolio Tracker", "tracker")
        self.backtests_button = SidebarButton(f"Backtests", "backtests")

        self.buttons = (
            self.home_button,
            self.equities_button,
            self.commodities_button,
            self.economics_button,
            self.tracker_button,
            self.backtests_button
        )
        for button in self.buttons:
            self.layout.addWidget(button)

        self.layout.addWidget(QFrame())

class SidebarButton(QPushButton):
    def __init__(self, text, icon_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(50)
        self.setText(f"   {text}")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setStyleSheet(
            sidebar_button_css.format(icon_name)
        )