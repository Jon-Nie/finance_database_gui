from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from stylesheets import (
    sidebar_css,
    sidebar_button_css,
    sidebar_placeholder_css,
    button_frame_css
)

class SideBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setFixedWidth(70)
        self.setStyleSheet(sidebar_css)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.placeholder_frame = QFrame()
        self.placeholder_frame.setMaximumHeight(80)
        self.placeholder_frame.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.layout.addWidget(self.placeholder_frame)

        self.button_frame = ButtonFrame()
        self.layout.addWidget(self.button_frame)
        
        self.placeholder_frame2 = QFrame()
        self.placeholder_frame2.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.layout.addWidget(self.placeholder_frame2)

class SidebarButton(QPushButton):
    def __init__(self, text, icon_name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.icon_name = icon_name

        self.setFixedHeight(60)
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setToolTip(text)

        self.setStyleSheet(
            sidebar_button_css.format(icon_name)
        )

class ButtonFrame(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.layout = QVBoxLayout(self)
        self.setStyleSheet(button_frame_css)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        self.placeholder_frame1 = QFrame()
        self.placeholder_frame1.setFixedHeight(20)
        self.placeholder_frame1.setStyleSheet(sidebar_placeholder_css)
        self.layout.addWidget(self.placeholder_frame1)

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
            button.clicked.connect(self.change_stylesheet)

        self.placeholder_frame2 = QFrame()
        self.placeholder_frame2.setFixedHeight(20)
        self.placeholder_frame2.setStyleSheet(sidebar_placeholder_css)
        self.layout.addWidget(self.placeholder_frame2)

        self.home_button.animateClick()
    
    def change_stylesheet(self):
        for button in self.buttons:
            button.setObjectName("inactive")
            button.setStyleSheet(sidebar_button_css.format(button.icon_name))

        sender = self.sender()
        if sender == self.home_button:
            sender.setObjectName("active_blue")
        else:
            sender.setObjectName("active")
        sender.setStyleSheet(sidebar_button_css.format(sender.icon_name))

        index = self.buttons.index(sender)
        if index == 0:
            self.placeholder_frame1.setObjectName("wrapper_top")
        else:
            self.placeholder_frame1.setObjectName("inactive")
            self.buttons[index-1].setObjectName("wrapper_top")
            self.buttons[index-1].setStyleSheet(sidebar_button_css.format(self.buttons[index-1].icon_name))
        if index == len(self.buttons)-1:
            self.placeholder_frame2.setObjectName("wrapper_bottom")
        else:
            self.placeholder_frame2.setObjectName("inactive")
            self.buttons[index+1].setObjectName("wrapper_bottom")
            self.buttons[index+1].setStyleSheet(sidebar_button_css.format(self.buttons[index+1].icon_name))
        self.placeholder_frame1.setStyleSheet(sidebar_placeholder_css)
        self.placeholder_frame2.setStyleSheet(sidebar_placeholder_css)
