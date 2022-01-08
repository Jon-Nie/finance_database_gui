from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class SideBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(200)
        self.setStyleSheet("background-color: #FFFFFF")

        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow_color = QColor("#565656")
        self.shadow_color.setAlpha(40)
        self.shadow.setColor(self.shadow_color)
        self.shadow.setOffset(5, 5)
        self.setGraphicsEffect(self.shadow)

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
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setFixedHeight(50)
        self.setText(text)
        self.icon_name = icon_name
        self.icon = QIcon(f"icons/{icon_name}_grey.svg")
        self.setIcon(self.icon)
        self.setIconSize(QSize(20, 20))
        self.setStyleSheet(
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
                icon: url(icons/{icon_name}_blue.svg)
            }}
            """
        )