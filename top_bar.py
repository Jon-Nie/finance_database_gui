from PySide2.QtCore import *
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from stylesheets import (
    topbar_css,
    search_box_css,
    minimize_css,
    maximize_css,
    close_css
)

class TopBar(QFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setFixedHeight(60)
        self.setStyleSheet(topbar_css)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(50, 0, 10, 0)
        self.layout.setSpacing(0)

        placeholder_frame = QFrame()
        self.layout.addWidget(placeholder_frame)

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search ...")
        self.search_box.setFixedWidth(250)
        self.search_box.setFixedHeight(40)
        self.search_box.setStyleSheet(search_box_css)
        self.layout.addWidget(self.search_box)

        self.minimize_button = QPushButton()
        self.minimize_button.setIconSize(QSize(16, 16))
        self.minimize_button.setFixedSize(40, 40)
        self.minimize_button.setStyleSheet(minimize_css)
        self.layout.addWidget(self.minimize_button)

        self.maximize_button = QPushButton()
        self.maximize_button.setIconSize(QSize(14, 14))
        self.maximize_button.setFixedSize(40, 40)
        self.maximize_button.setStyleSheet(maximize_css)
        self.layout.addWidget(self.maximize_button)

        self.close_button = QPushButton()
        self.close_button.setFixedSize(40, 40)
        self.close_button.setStyleSheet(close_css)
        self.layout.addWidget(self.close_button)