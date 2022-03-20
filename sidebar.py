from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from stylesheets import (
    sidebar_css,
    sidebar_button_css,
    sidebar_button_sub_css,
    sidebar_button_super_css
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
        self.equities_button = SidebarButtonSuper(f"Equities", "equities")
        self.stocks_button = SidebarButtonSub(f"Stocks")
        self.industries_button = SidebarButtonSub(f"Industries")
        self.analysts_button = SidebarButtonSub(f"Analysts")
        self.institutionals_button = SidebarButtonSub(f"Investment Managers")
        self.factors_button = SidebarButtonSub(f"Equity Factors")
        self.commodities_button = SidebarButton(f"Commodities", "commodities")
        self.economics_button = SidebarButton(f"Economic Data", "economics")
        self.tracker_button = SidebarButton(f"Portfolio Tracker", "tracker")
        self.backtests_button = SidebarButton(f"Backtests", "backtests")

        self.buttons = (
            self.home_button,
            self.equities_button,
            self.stocks_button,
            self.industries_button,
            self.analysts_button,
            self.institutionals_button,
            self.factors_button,
            self.commodities_button,
            self.economics_button,
            self.tracker_button,
            self.backtests_button
        )
        for button in self.buttons:
            self.layout.addWidget(button)

        self.layout.addWidget(QFrame())
    
    def animation(self, button, start, end):
        button.animation = QPropertyAnimation(button, b"maximumHeight")
        button.animation.setDuration(100)
        button.animation.setStartValue(start)
        button.animation.setEndValue(end)
        button.animation.setEasingCurve(QEasingCurve.Linear)
        button.animation.start()


class SidebarButton(QPushButton):
    def __init__(self, text, icon_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(50)
        self.setText(f"   {text}")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setStyleSheet(
            sidebar_button_css.format(icon_name)
        )

class SidebarButtonSuper(QPushButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(50)
        self.setText(f"   {text}")
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setStyleSheet(
            sidebar_button_super_css
        )


class SidebarButtonSub(QPushButton):
    def __init__(self, text, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setMinimumHeight(0)
        self.setMaximumHeight(35)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum))

        self.setText(text)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        self.setStyleSheet(
            sidebar_button_sub_css
        )